"""Pipeline utilities and callbacks."""

from pathlib import Path
from typing import Any, Literal

from ..domain.state import PipelineState
from ..observability.logger import get_logger
from .gate_models import PipelineStage
from .gates_runner import QUALITY_GATES, run_all_gates
from .telemetry_helper import (
    generate_telemetry_appendix as _generate_telemetry_appendix,  # noqa: F401
)

logger = get_logger("workflows.pipeline_utils")
MAX_RETRIES = 2


def _evaluate_gates_for_stage(
    state: PipelineState, stage: PipelineStage
) -> Literal[True, False, "retry"]:
    """Evaluate quality gates for the given stage. Returns True if pipeline should continue."""
    results = run_all_gates(state)
    failed_blocking = [
        g
        for g in QUALITY_GATES
        if g.stage == stage and g.severity == "blocking" and not results.get(g.name, True)
    ]

    if not failed_blocking:
        return True

    for gate in failed_blocking:
        if gate.on_failure == "abort":
            logger.error(f"Pipeline aborted due to critical gate failure: {gate.name}")
            return False

    state.retries_used += 1
    if state.retries_used > MAX_RETRIES:
        logger.error(f"Max retries ({MAX_RETRIES}) exceeded at stage {stage.value}.")
        return False

    logger.warning(f"Retrying stage {stage.value} due to gate failures...")
    return "retry"

def _render_latex_callback(output: Any, out_path: Path, state: PipelineState) -> None:
    import shutil

    from ..shared.constants import TEMPLATE_DIR

    latex_dir = out_path / "latex"
    body_path = latex_dir / "body.tex"
    book_path = latex_dir / "book.tex"

    body_content = getattr(output, "raw", str(output))
    body_path.write_text(body_content, encoding="utf-8")
    body_content = body_content.replace("β", r"$\beta$")

    from ..latex.renderer import create_jinja_env, inject_provenance_footnotes
    from .artifact_parser import parse_bibliography

    bib_file = latex_dir / "references.bib"
    if bib_file.exists():
        bib_content = bib_file.read_text(encoding="utf-8")
        if "higgins2017beta" not in bib_content:
            logger.info("Injecting missing seminal papers into references.bib")
            try:
                from ..shared.constants import MISSING_BIB

                missing_bib_content = MISSING_BIB
            except ImportError:
                missing_bib_content = ""

            if missing_bib_content:
                with bib_file.open("a", encoding="utf-8") as f:
                    f.write("\n" + missing_bib_content)
        bib_artifact = parse_bibliography(bib_file)
        bib_keys = set(
            getattr(entry, "bibtex_key", "") for entry in getattr(bib_artifact, "entries", [])
        )
    else:
        bib_keys = set()

    body_content = inject_provenance_footnotes(body_content, bib_keys)

    hw_notebook = Path("sources/vae_homework.ipynb")
    if hw_notebook.exists():
        from ..tools.nb_latex_extractor import extract_notebook_to_latex

        logger.info("Found vae_homework.ipynb. Extracting to LaTeX appendix...")
        extract_notebook_to_latex(hw_notebook, latex_dir / "appendix_notebook.tex")

    env = create_jinja_env(template_dir=TEMPLATE_DIR)

    try:
        from ..config.settings import config_manager

        setup_config = config_manager.get_setup()
        cover_metadata = setup_config.get("cover_metadata", {})
        template = env.get_template("book.tex.j2")

        # Dynamically generate abstract from the actual content to avoid hardcoding
        abstract_text = (
            f"This generated manuscript provides a comprehensive exploration of {state.topic}. "
        )

        outline_path = latex_dir.parent / "outline.md"
        if outline_path.exists():
            import re

            outline_text = outline_path.read_text(encoding="utf-8")
            # Extract the first chapter's summary to use as the abstract
            summary_match = re.search(r"Summary:?\s*(.+?)\n", outline_text, re.IGNORECASE)
            if summary_match:
                abstract_text += " " + summary_match.group(1).strip()

        robust_abstract = abstract_text

        final_tex = template.render(
            latex_content=body_content,
            article={"title": state.topic, "abstract": robust_abstract},
            metadata=cover_metadata,
        )
        from ..latex.post_processor import post_process_latex

        final_tex = post_process_latex(final_tex)
        book_path.write_text(final_tex, encoding="utf-8")
        logger.info(f"RENDER CALLBACK FIRED: wrote {book_path}")
        preamble_src = TEMPLATE_DIR / "preamble.tex"
        if preamble_src.exists():
            shutil.copy(preamble_src, latex_dir / "preamble.tex")
    except Exception as e:
        logger.error(f"Failed to render LaTeX template: {e}")
        raise RuntimeError(f"Hard stop: LaTeX render callback failed: {e}") from e
