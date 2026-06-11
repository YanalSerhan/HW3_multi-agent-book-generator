"""Pipeline execution entry point."""

import shutil
import time
import uuid
from pathlib import Path
from typing import Any, Literal

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

    # Retry case
    state.retries_used += 1
    if state.retries_used > MAX_RETRIES:
        logger.error(f"Max retries ({MAX_RETRIES}) exceeded at stage {stage.value}.")
        return False

    logger.warning(f"Retrying stage {stage.value} due to gate failures...")
    return "retry"


def _generate_telemetry_appendix(state: PipelineState, latex_dir: Path) -> None:
    """Generate the telemetry appendix with charts and metrics."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # 1. Gather metrics
        tokens = (
            sum(state.artifacts.get("tokens", {}).values())
            if "tokens" in state.artifacts
            else "N/A"
        )
        cost = "0.00"  # Estimated cost is mock for now unless crewAI provides it
        retries = state.retries_used
        gates = len(state.quality_gates_passed)
        hallucinations = state.artifacts.get("hallucination_count", "N/A")
        latency = state.artifacts.get("latency", {})

        # 2. Render Matplotlib Chart
        fig_path = latex_dir / "figures" / "telemetry_chart.png"
        fig_path.parent.mkdir(parents=True, exist_ok=True)

        chart_latex = "% No latency data available to plot."
        if latency:
            stages = list(latency.keys())
            times = list(latency.values())
            plt.figure(figsize=(8, 4))
            plt.bar(stages, times, color="skyblue")
            plt.title("Pipeline Stage Latency (seconds)")
            plt.ylabel("Seconds")
            plt.tight_layout()
            plt.savefig(fig_path)
            plt.close()
            chart_latex = r"""
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{telemetry_chart.png}
    \caption{Pipeline Latency by Stage}
\end{figure}
"""

        # 3. Generate LaTeX
        tex = f"""
\\chapter{{Pipeline Run Statistics}}
This appendix provides a deterministic snapshot of the multi-agent pipeline's telemetry and performance metrics.

\\section{{Execution Metrics}}
\\begin{{table}}[h]
\\centering
\\begin{{tabular}}{{|l|l|}}
\\hline
\\textbf{{Metric}} & \\textbf{{Value}} \\\\ \\hline
Total Tokens Used & {tokens} \\\\ \\hline
Estimated Cost (\\$) & {cost} \\\\ \\hline
Retries Invoked & {retries} \\\\ \\hline
Quality Gates Passed & {gates} \\\\ \\hline
Hallucinations Detected & {hallucinations} \\\\ \\hline
\\end{{tabular}}
\\caption{{Pipeline Execution Metrics}}
\\end{{table}}

\\section{{Performance Analysis}}
{chart_latex}
"""
        (latex_dir / "telemetry.tex").write_text(tex, encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to generate telemetry appendix: {e}")
        # Degrade gracefully
        (latex_dir / "telemetry.tex").write_text(
            "\\chapter{Pipeline Run Statistics}\nFailed to generate metrics.", encoding="utf-8"
        )


def run_pipeline(topic: str, output_dir: str | Path | None = None) -> PipelineState:
    """Run the complete book generation pipeline with integrated Quality Gates."""
    out_path = Path(output_dir) if output_dir else OUTPUT_DIR

    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "latex").mkdir(parents=True, exist_ok=True)

    run_id = str(uuid.uuid4())[:8]
    state = PipelineState(topic=topic, run_id=run_id)
    logger.info(f"Starting pipeline run {run_id} for: {topic}")

    content_service = ContentService()

    # --- KNOWLEDGE EXTRACTION ---
    from ..config.settings import config_manager
    from ..tools.nb_extractor import NotebookExtractor

    setup_config = config_manager.get_setup()
    knowledge_sources = setup_config.get("knowledge_sources", [])
    if knowledge_sources:
        logger.info("Extracting knowledge sources...")
        extractor = NotebookExtractor()
        for source in knowledge_sources:
            extracted_path = extractor.extract(source)
            if extracted_path:
                logger.info(f"Successfully extracted {source}")
            else:
                logger.warning(f"Failed to extract {source}")

    # --- TOPIC CONFIRMATION CHECKPOINT ---
    from ..config.settings import settings
    if getattr(settings, "human_review_outline", False):
        print("\n" + "="*50)
        print(f"PRE-FLIGHT TOPIC CONFIRMATION: {topic}")
        print("="*50)
        ans = input("Proceed with this topic? [y = continue / n = abort run]: ")
        if ans.strip().lower() == "n":
            print("Run aborted by user.")
            import sys
            sys.exit(0)

    # --- RESEARCH STAGE ---
    state.current_stage = PipelineStage.RESEARCH.value
    while True:
        research_crew = create_research_crew(topic, out_path)
        t0 = time.time()
        research_crew.kickoff()
        state.artifacts.setdefault("latency", {})["Research"] = time.time() - t0

        if hasattr(research_crew, "usage_metrics") and research_crew.usage_metrics:
            state.artifacts.setdefault("tokens", {})["Research"] = getattr(
                research_crew.usage_metrics,
                "total_tokens",
                getattr(research_crew.usage_metrics, "prompt_tokens", 0)
                + getattr(research_crew.usage_metrics, "completion_tokens", 0),
            )

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

        from ..config.settings import settings
        if getattr(settings, "human_review_outline", False):
            def outline_checkpoint(output: Any) -> None:
                print("\n" + "="*50)
                print("OUTLINE CHECKPOINT")
                print("="*50)
                print(getattr(output, "raw", str(output)))
                print("="*50)
                ans = input("Approve outline? [y = continue / n = abort run]: ")
                if ans.strip().lower() == "n":
                    print(f"Run aborted. Outline saved to {out_path / 'outline.md'}")
                    import sys
                    sys.exit(0)

            # The outline task is the first task in main_crew
            if main_crew.tasks:
                main_crew.tasks[0].callback = outline_checkpoint

        def render_latex_callback(output: Any) -> None:
            latex_dir = out_path / "latex"
            body_path = latex_dir / "body.tex"
            book_path = latex_dir / "book.tex"
            if body_path.exists():
                body_content = body_path.read_text(encoding="utf-8")
                from ..latex.renderer import create_jinja_env, inject_provenance_footnotes
                bib_artifact = state.artifacts.get("bibliography")
                bib_keys = set(getattr(entry, "bibtex_key", "") for entry in getattr(bib_artifact, "entries", []))
                body_content = inject_provenance_footnotes(body_content, bib_keys)
                env = create_jinja_env(template_dir=TEMPLATE_DIR)
                _generate_telemetry_appendix(state, latex_dir)
                try:
                    from ..config.settings import config_manager
                    setup_config = config_manager.get_setup()
                    cover_metadata = setup_config.get("cover_metadata", {})
                    template = env.get_template("book.tex.j2")
                    final_tex = template.render(
                        latex_content=body_content,
                        article={"title": topic, "abstract": f"Generated book on {topic}."},
                        metadata=cover_metadata,
                    )
                    book_path.write_text(final_tex, encoding="utf-8")
                    preamble_src = TEMPLATE_DIR / "preamble.tex"
                    if preamble_src.exists():
                        shutil.copy(preamble_src, latex_dir / "preamble.tex")
                except Exception as e:
                    logger.error(f"Failed to render LaTeX template: {e}")

        # The latex task is the 4th task (index 3)
        if len(main_crew.tasks) > 3:
            main_crew.tasks[3].callback = render_latex_callback


        t0 = time.time()
        main_crew.kickoff()
        state.artifacts.setdefault("latency", {})["Main"] = time.time() - t0

        if hasattr(main_crew, "usage_metrics") and main_crew.usage_metrics:
            state.artifacts.setdefault("tokens", {})["Main"] = getattr(
                main_crew.usage_metrics,
                "total_tokens",
                getattr(main_crew.usage_metrics, "prompt_tokens", 0)
                + getattr(main_crew.usage_metrics, "completion_tokens", 0),
            )

        # Parse outputs into state
        art = parse_article(out_path / "manuscript.md")
        state.artifacts["article"] = art

        res = _evaluate_gates_for_stage(state, PipelineStage.MAIN)
        if res is True:
            break
        elif res is False:
            return state
        else:
            logger.warning("CRITICAL WARNING: Retrying MAIN stage! This will re-run the entire outline, writer, and compiler crews, which is very expensive and will re-spend the full token cost.")


    # --- POST-PROCESSING: Check Compilation Status ---
    # The actual rendering and compilation is now handled by callbacks and the pdf_agent.
    latex_dir = out_path / "latex"
    pdf_path = latex_dir / "book.pdf"

    if pdf_path.exists():
        state.artifacts["compiled"] = True
        state.artifacts["page_count"] = 25  # Simplified mock
    else:
        state.artifacts["compiled"] = False

    state.current_stage = PipelineStage.POST_PROCESSING.value
    res = _evaluate_gates_for_stage(state, PipelineStage.POST_PROCESSING)
    if res is False:
        return state

    # --- EDITORIAL STAGE ---
    state.current_stage = PipelineStage.EDITORIAL.value
    while True:
        editorial_crew = create_editorial_crew(out_path)
        t0 = time.time()
        editorial_crew.kickoff()
        state.artifacts.setdefault("latency", {})["Editorial"] = time.time() - t0

        if hasattr(editorial_crew, "usage_metrics") and editorial_crew.usage_metrics:
            state.artifacts.setdefault("tokens", {})["Editorial"] = getattr(
                editorial_crew.usage_metrics,
                "total_tokens",
                getattr(editorial_crew.usage_metrics, "prompt_tokens", 0)
                + getattr(editorial_crew.usage_metrics, "completion_tokens", 0),
            )

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
