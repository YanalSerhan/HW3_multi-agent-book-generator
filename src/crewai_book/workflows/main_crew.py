"""Main crew orchestrating the full book generation pipeline.

Coordinates all 10 agents through the sequential pipeline stages:
research → outline → writing → editorial → citation → LaTeX → PDF → QA.
"""

import uuid

from crewai import Crew, Process, Task

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


def create_main_crew(topic: str) -> Crew:
    """Build the main sequential pipeline crew.

    Orchestrates the full pipeline from research through QA,
    coordinating sub-crews and individual agents in dependency order.
    """
    logger.info(f"Building main pipeline for topic: {topic}")

    outline_agent = create_outline_agent()
    writer_agent = create_writer_agent()
    latex_agent = create_latex_agent()
    pdf_agent = create_pdf_agent()
    qa_agent = create_qa_agent()

    outline_task = Task(
        description=(
            f"Create a detailed book outline for '{topic}' with "
            "6-8 chapters, each having 3-5 sections. Include a chapter "
            "summary and target word count for each section."
        ),
        expected_output="Hierarchical outline with chapters and sections.",
        agent=outline_agent,
    )

    writing_task = Task(
        description=(
            "Write the complete manuscript following the outline. "
            "Each section should be 500-800 words with proper citations. "
            "Maintain consistent voice and graduate-level readability."
        ),
        expected_output="Complete manuscript text for all chapters.",
        agent=writer_agent,
    )

    latex_task = Task(
        description=(
            "Convert the manuscript into LaTeX source using the memoir "
            "class. Structure it as a compilable book with all required "
            "packages, bibliography, and formatting."
        ),
        expected_output="Complete LaTeX source files ready for compilation.",
        agent=latex_agent,
    )

    pdf_task = Task(
        description=(
            "Compile the LaTeX source into a final PDF. Verify the "
            "output has ≥20 pages and all elements render correctly."
        ),
        expected_output="Compiled PDF with quality verification report.",
        agent=pdf_agent,
    )

    qa_task = Task(
        description=(
            "Perform final quality certification. Run all quality gates "
            "and produce a comprehensive QA report confirming the "
            "manuscript meets all publication standards."
        ),
        expected_output="QA certification report with gate results.",
        agent=qa_agent,
    )

    return Crew(
        agents=[outline_agent, writer_agent, latex_agent, pdf_agent, qa_agent],
        tasks=[outline_task, writing_task, latex_task, pdf_task, qa_task],
        process=Process.sequential,
        verbose=True,
    )


def run_pipeline(topic: str) -> PipelineState:
    """Run the complete book generation pipeline.

    Executes the research sub-crew, then the main crew stages,
    with the editorial sub-crew integrated into the review phase.

    Args:
        topic: The book topic to generate.

    Returns:
        The final PipelineState after all stages complete.
    """
    run_id = str(uuid.uuid4())[:8]
    state = PipelineState(topic=topic, run_id=run_id)
    logger.info(f"Starting pipeline run {run_id} for: {topic}")

    state.current_stage = "research"
    research_crew = create_research_crew(topic)
    research_crew.kickoff()

    state.current_stage = "main"
    main_crew = create_main_crew(topic)
    main_crew.kickoff()

    state.current_stage = "editorial"
    editorial_crew = create_editorial_crew()
    editorial_crew.kickoff()

    state.current_stage = "complete"
    logger.info(f"Pipeline run {run_id} completed successfully.")

    return state
