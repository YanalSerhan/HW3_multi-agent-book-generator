"""Main crew orchestrating the full book generation pipeline.

Coordinates all 10 agents through the sequential pipeline stages:
research → outline → writing → editorial → citation → LaTeX → PDF → QA.
"""

import uuid
from pathlib import Path

from crewai import Crew, Process, Task

from ..agents.figure_agent import create_figure_agent
from ..agents.latex_agent import create_latex_agent
from ..agents.outline_agent import create_outline_agent
from ..agents.pdf_agent import create_pdf_agent
from ..agents.qa_agent import create_qa_agent
from ..agents.writer_agent import create_writer_agent
from ..domain.state import PipelineState
from ..observability.logger import get_logger
from .editorial_crew import create_editorial_crew
from .research_crew import create_research_crew

logger = get_logger("workflows.main_crew")


def create_main_crew(topic: str, output_dir: Path) -> Crew:
    """Build the main sequential pipeline crew.

    Orchestrates the full pipeline from research through QA,
    coordinating sub-crews and individual agents in dependency order.
    """
    logger.info(f"Building main pipeline for topic: {topic}")

    outline_agent = create_outline_agent()
    writer_agent = create_writer_agent()
    figure_agent = create_figure_agent()
    latex_agent = create_latex_agent()
    pdf_agent = create_pdf_agent()
    qa_agent = create_qa_agent()

    outline_task = Task(
        description=(
            f"Create a detailed book outline for '{topic}' with "
            "12-15 chapters, each having 4-6 sections. Include a chapter "
            "summary and target word count for each section."
        ),
        expected_output="Hierarchical outline with chapters and sections.",
        output_file=str(output_dir / "outline.md"),
        agent=outline_agent,
    )

    writing_task = Task(
        description=(
            "Write the complete manuscript following the outline. "
            "Each section should be 800-1000 words with proper citations. "
            "Maintain consistent voice and graduate-level readability."
        ),
        expected_output="Complete manuscript text for all chapters.",
        output_file=str(output_dir / "manuscript.md"),
        agent=writer_agent,
    )

    figure_task = Task(
        description=(
            "Read the manuscript and identify 3 key concepts or architectures that "
            "would benefit from visualization. Generate 3 professional figures "
            "(e.g., bar charts, line plots, or block diagrams) using the figure generator tool. "
            "Save them as PNG or PDF files. Provide a summary of the generated figures "
            "including their filenames and suggested captions."
        ),
        expected_output="A list of generated figures with their filenames and captions.",
        output_file=str(output_dir / "figures_report.md"),
        agent=figure_agent,
    )

    latex_task = Task(
        description=(
            "Convert the manuscript and figures report into LaTeX source. "
            "Convert all Markdown tables into proper LaTeX \\begin{table} environments. To prevent table overflow, MUST use \\resizebox{\\textwidth}{!}{...} around your tabular environments. "
            "CRITICAL: Output ONLY the raw LaTeX source code for the chapters and sections. "
            "Do NOT output \\documentclass, \\begin{document}, or any preamble. Just output the \\chapter, \\section, and text content. "
            "Do NOT enclose your output in markdown code blocks."
        ),
        expected_output="Raw LaTeX body code containing only chapters, sections, and properly formatted tables.",
        output_file=str(output_dir / "latex" / "body.tex"),
        agent=latex_agent,
    )

    pdf_task = Task(
        description=(
            "Compile the LaTeX source into a final PDF. Verify the "
            "output has ≥20 pages and all elements render correctly."
        ),
        expected_output="Compiled PDF with quality verification report.",
        output_file=str(output_dir / "latex" / "pdf_report.md"),
        agent=pdf_agent,
    )

    qa_task = Task(
        description=(
            "Perform final quality certification. Run all quality gates "
            "and produce a comprehensive QA report confirming the "
            "manuscript meets all publication standards."
        ),
        expected_output="QA certification report with gate results.",
        output_file=str(output_dir / "qa_report.md"),
        agent=qa_agent,
    )

    return Crew(
        agents=[outline_agent, writer_agent, figure_agent, latex_agent, pdf_agent, qa_agent],
        tasks=[outline_task, writing_task, figure_task, latex_task, pdf_task, qa_task],
        process=Process.sequential,
        verbose=True,
    )


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
    from pathlib import Path

    if output_dir is None:
        from ..shared.constants import OUTPUT_DIR
        out_path = OUTPUT_DIR
    else:
        out_path = Path(output_dir)

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
    import shutil
    from jinja2 import Environment, FileSystemLoader
    from ..shared.constants import TEMPLATE_DIR
    
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
                article={"title": topic, "abstract": f"An automatically generated book on {topic}."}
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
