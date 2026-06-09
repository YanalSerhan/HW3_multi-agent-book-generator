"""Editorial sub-crew for the book generation pipeline.

Orchestrates agents A-05 (Editor) and A-06 (Reviewer)
in a hierarchical crew for multi-pass editorial review.
"""

from pathlib import Path

from crewai import Crew, Process, Task

from ..agents.editor_agent import create_editor_agent
from ..agents.reviewer_agent import create_reviewer_agent
from ..observability.logger import get_logger

logger = get_logger("workflows.editorial_crew")


def create_editorial_crew(output_dir: Path) -> Crew:
    """Build and return the editorial sub-crew.

    This crew uses hierarchical process where a manager LLM
    orchestrates the editor and reviewer to perform a multi-pass
    editorial review, improving prose quality and catching issues
    before final typesetting.
    """
    editor_agent = create_editor_agent()
    reviewer_agent = create_reviewer_agent()

    editing_task = Task(
        description=(
            "Edit the manuscript for clarity, consistency, and grammar. "
            "Check readability score for each section and ensure it "
            "meets the ≥60 Flesch target. Fix any issues found."
        ),
        expected_output="Edited manuscript with improvement notes.",
        output_file=str(output_dir / "manuscript_edited.md"),
        agent=editor_agent,
    )

    review_task = Task(
        description=(
            "Conduct a peer review of the edited manuscript. Evaluate "
            "content depth, accuracy, logical flow, and completeness. "
            "Provide a structured review report with actionable feedback."
        ),
        expected_output="Structured review report with recommendations.",
        output_file=str(output_dir / "review_report.md"),
        agent=reviewer_agent,
    )

    logger.info("Creating editorial crew")

    return Crew(
        agents=[editor_agent, reviewer_agent],
        tasks=[editing_task, review_task],
        process=Process.hierarchical,
        manager_llm="gpt-4o",
        verbose=True,
    )
