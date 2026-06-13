"""Main crew orchestrating the full book generation pipeline.

Coordinates all 10 agents through the sequential pipeline stages:
research → outline → writing → editorial → citation → LaTeX → PDF → QA.
"""

from pathlib import Path

from crewai import Crew, Process

from ..agents.figure_agent import create_figure_agent
from ..agents.latex_agent import create_latex_agent
from ..agents.outline_agent import create_outline_agent
from ..agents.pdf_agent import create_pdf_agent
from ..agents.qa_agent import create_qa_agent
from ..agents.writer_agent import create_writer_agent
from ..observability.logger import get_logger

logger = get_logger("workflows.main_crew")


def create_main_crew(topic: str, output_dir: Path) -> Crew:
    """Build the main sequential pipeline crew.

    Orchestrates the full pipeline from research through QA,
    coordinating sub-crews and individual agents in dependency order.
    """
    logger.info(f"Building main pipeline for topic: {topic}")

    outline_agent = create_outline_agent()
    writer_agent = create_writer_agent()
    figure_agent = create_figure_agent(output_dir=output_dir)
    latex_agent = create_latex_agent()
    pdf_agent = create_pdf_agent()
    qa_agent = create_qa_agent()

    from ..config.settings import config_manager

    setup_config = config_manager.get_setup()
    book_length = setup_config.get("book_length", {})
    chapter_count = book_length.get("chapter_count", 8)
    words_per_section = book_length.get("words_per_section", 200)

    from .main_tasks import (
        get_figure_task,
        get_latex_task,
        get_outline_task,
        get_pdf_task,
        get_provenance_task,
        get_qa_task,
        get_writing_task,
    )

    outline_task = get_outline_task(
        topic, chapter_count, words_per_section, output_dir, outline_agent
    )
    writing_task = get_writing_task(words_per_section, output_dir, writer_agent)
    provenance_task = get_provenance_task(output_dir, writer_agent)
    figure_task = get_figure_task(output_dir, figure_agent)
    latex_task = get_latex_task(output_dir, latex_agent)
    pdf_task = get_pdf_task(output_dir, pdf_agent)
    qa_task = get_qa_task(output_dir, qa_agent)

    tasks_list = [
        outline_task,
        writing_task,
        provenance_task,
        figure_task,
        latex_task,
        pdf_task,
        qa_task,
    ]

    for task in tasks_list:
        if (
            "LaTeX source" in task.description
            or "Convert the manuscript and figures" in task.description
        ):
            # We will handle callback in pipeline_stages
            pass

    return Crew(
        agents=[outline_agent, writer_agent, figure_agent, latex_agent, pdf_agent, qa_agent],
        tasks=tasks_list,
        process=Process.sequential,
        verbose=True,
    )
