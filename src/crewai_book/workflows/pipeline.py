"""Pipeline execution entry point."""

import shutil
import uuid
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..domain.state import PipelineState
from ..observability.logger import get_logger
from ..shared.constants import OUTPUT_DIR, TEMPLATE_DIR
from .editorial_crew import create_editorial_crew
from .main_crew import create_main_crew
from .research_crew import create_research_crew

logger = get_logger("workflows.pipeline")


def run_pipeline(topic: str, output_dir: str | Path | None = None) -> PipelineState:
    """Run the complete book generation pipeline.

    Executes the research sub-crew, then the main crew stages,
    with the editorial sub-crew integrated into the review phase.

    Args:
        topic: The book topic to generate.
        output_dir: The directory to save generated artifacts.

    Returns:
        The final PipelineState after all stages complete.
    """
    out_path = Path(output_dir) if output_dir else OUTPUT_DIR

    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "latex").mkdir(parents=True, exist_ok=True)

    run_id = str(uuid.uuid4())[:8]
    state = PipelineState(topic=topic, run_id=run_id)
    logger.info(f"Starting pipeline run {run_id} for: {topic}")

    state.current_stage = "research"
    research_crew = create_research_crew(topic, out_path)
    research_crew.kickoff()

    state.current_stage = "main"
    main_crew = create_main_crew(topic, out_path)
    main_crew.kickoff()

    # --- POST-PROCESSING: Render the Final LaTeX Book ---
    latex_dir = out_path / "latex"
    body_path = latex_dir / "body.tex"
    book_path = latex_dir / "book.tex"

    if body_path.exists():
        # Load the generated body
        body_content = body_path.read_text(encoding='utf-8')

        # Load the jinja template
        env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        try:
            template = env.get_template("book.tex.j2")
            final_tex = template.render(
                latex_content=body_content,
                article={"title": topic, "abstract": f"An automatically generated book on {topic}."}  # noqa: E501
            )
            book_path.write_text(final_tex, encoding='utf-8')
            logger.info("Successfully rendered book.tex from Jinja template.")
        except Exception as e:
            logger.error(f"Failed to render Jinja template: {e}")

        # Ensure preamble is copied
        preamble_src = TEMPLATE_DIR / "preamble.tex"
        if preamble_src.exists():
            shutil.copy(preamble_src, latex_dir / "preamble.tex")

    state.current_stage = "editorial"
    editorial_crew = create_editorial_crew(out_path)
    editorial_crew.kickoff()

    state.current_stage = "complete"
    logger.info(f"Pipeline run {run_id} completed successfully.")

    return state
