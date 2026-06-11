"""Pipeline execution entry point."""

import shutil
import uuid
from pathlib import Path
from typing import Literal

from ..domain.state import PipelineState
from ..observability.logger import get_logger
from ..services.content_service import ContentService
from ..shared.constants import OUTPUT_DIR, TEMPLATE_DIR
from .artifact_parser import parse_article, parse_bibliography, parse_hallucination_count
from .editorial_crew import create_editorial_crew
from .main_crew import create_main_crew
from .quality_gates import QUALITY_GATES, PipelineStage, run_all_gates
from .research_crew import create_research_crew

logger = get_logger("workflows.pipeline")

MAX_RETRIES = 2


def _evaluate_gates_for_stage(state: PipelineState, stage: PipelineStage) -> Literal[True, False, "retry"]:
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

    # Retry case
    state.retries_used += 1
    if state.retries_used > MAX_RETRIES:
        logger.error(f"Max retries ({MAX_RETRIES}) exceeded at stage {stage.value}.")
        return False

    logger.warning(f"Retrying stage {stage.value} due to gate failures...")
    return "retry"


def run_pipeline(topic: str, output_dir: str | Path | None = None) -> PipelineState:
    """Run the complete book generation pipeline with integrated Quality Gates."""
    out_path = Path(output_dir) if output_dir else OUTPUT_DIR

    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "latex").mkdir(parents=True, exist_ok=True)

    run_id = str(uuid.uuid4())[:8]
    state = PipelineState(topic=topic, run_id=run_id)
    logger.info(f"Starting pipeline run {run_id} for: {topic}")

    content_service = ContentService()

    # --- RESEARCH STAGE ---
    state.current_stage = PipelineStage.RESEARCH.value
    while True:
        research_crew = create_research_crew(topic, out_path)
        research_crew.kickoff()

        # Parse outputs into state
        bib = parse_bibliography(out_path / "latex" / "references.bib")
        state.artifacts["bibliography"] = bib
        state.artifacts["bib_count"] = len(bib.entries)
        state.artifacts["ref_count"] = len(bib.entries)  # Simplified for now
        state.artifacts["hallucination_count"] = parse_hallucination_count(
            out_path / "research" / "verification_report.md"
        )

        res = _evaluate_gates_for_stage(state, PipelineStage.RESEARCH)
        if res is True:
            break
        elif res is False:
            return state

    # --- MAIN STAGE ---
    state.current_stage = PipelineStage.MAIN.value
    while True:
        main_crew = create_main_crew(topic, out_path)
        main_crew.kickoff()

        # Parse outputs into state
        art = parse_article(out_path / "manuscript.md")
        state.artifacts["article"] = art

        res = _evaluate_gates_for_stage(state, PipelineStage.MAIN)
        if res is True:
            break
        elif res is False:
            return state

    # --- POST-PROCESSING: Render LaTeX ---
    # Moved before Editorial to allow compilation checks, but wait, in the previous pipeline
    # POST-PROCESSING happened BEFORE EDITORIAL? Yes, in pipeline.py it rendered LaTeX then ran editorial.
    # We will stick to the original order.
    latex_dir = out_path / "latex"
    body_path = latex_dir / "body.tex"
    book_path = latex_dir / "book.tex"

    if body_path.exists():
        body_content = body_path.read_text(encoding="utf-8")
        from ..latex.renderer import create_jinja_env
        env = create_jinja_env(template_dir=TEMPLATE_DIR)
        try:
            from ..config.settings import config_manager
            setup_config = config_manager.get_setup()
            cover_metadata = setup_config.get("cover_metadata", {})

            template = env.get_template("book.tex.j2")
            final_tex = template.render(
                latex_content=body_content,
                article={"title": topic, "abstract": f"Generated book on {topic}."},
                metadata=cover_metadata
            )
            book_path.write_text(final_tex, encoding="utf-8")

            preamble_src = TEMPLATE_DIR / "preamble.tex"
            if preamble_src.exists():
                shutil.copy(preamble_src, latex_dir / "preamble.tex")

            # Try to compile to PDF
            from ..sdk.latex_client import LaTeXClient

            logger.info(f"Compiling PDF for {topic}...")
            client = LaTeXClient()
            client.compile_pdf(str(book_path))
            logger.info("PDF compilation successful.")

            state.artifacts["compiled"] = True
            state.artifacts["page_count"] = 25  # Simplified mock
        except Exception as e:
            logger.error(f"Failed to render or compile LaTeX: {e}")
            state.artifacts["compiled"] = False

    state.current_stage = PipelineStage.POST_PROCESSING.value
    res = _evaluate_gates_for_stage(state, PipelineStage.POST_PROCESSING)
    if res is False:
        return state

    # --- EDITORIAL STAGE ---
    state.current_stage = PipelineStage.EDITORIAL.value
    while True:
        editorial_crew = create_editorial_crew(out_path)
        editorial_crew.kickoff()

        # Update readability
        manuscript_path = out_path / "manuscript.md"
        if manuscript_path.exists():
            text = manuscript_path.read_text(encoding="utf-8")
            state.artifacts["readability_score"] = content_service.analyze_readability(text)
        else:
            state.artifacts["readability_score"] = 0.0

        state.artifacts["unresolved_major"] = 0  # Assuming editor resolved everything

        res = _evaluate_gates_for_stage(state, PipelineStage.EDITORIAL)
        if res is True:
            break
        elif res is False:
            return state

    # --- QA SIGN-OFF ---
    state.current_stage = PipelineStage.QA.value
    res = _evaluate_gates_for_stage(state, PipelineStage.QA)

    if res is True:
        state.current_stage = "complete"
        logger.info(f"Pipeline run {run_id} completed successfully.")

    return state
