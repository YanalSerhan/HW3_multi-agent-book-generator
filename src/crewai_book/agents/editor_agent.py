"""Editor Agent (A-05) — Senior Copy Editor.

Reviews and improves the manuscript for clarity, consistency,
grammar, and adherence to readability standards.
"""

from crewai import Agent

from ..tools.readability_tool import ReadabilityScoreTool


def create_editor_agent() -> Agent:
    """Create and return the Editor Agent.

    This agent performs comprehensive copy editing, improving prose
    quality, fixing grammatical issues, and ensuring each section
    meets the target readability score.
    """
    return Agent(
        role="Senior Copy Editor",
        goal=(
            "Edit the manuscript for clarity, consistency, and correctness. "
            "Ensure readability score ≥60, fix all grammatical errors, and "
            "maintain a consistent voice and terminology throughout."
        ),
        backstory=(
            "You are a senior copy editor at a major academic publisher "
            "with 20 years of experience editing technical manuscripts. "
            "You have an eye for inconsistency and a talent for making "
            "complex prose more accessible without losing precision."
        ),
        tools=[ReadabilityScoreTool()],
        verbose=True,
        allow_delegation=False,
    )
