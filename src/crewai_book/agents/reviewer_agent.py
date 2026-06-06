"""Reviewer Agent (A-06) — Peer Reviewer.

Performs structured peer review of the manuscript, identifying
weaknesses, gaps, and areas that need strengthening.
"""

from crewai import Agent

from ..tools.readability_tool import ReadabilityScoreTool


def create_reviewer_agent() -> Agent:
    """Create and return the Reviewer Agent.

    This agent simulates an academic peer review, providing
    structured feedback on content depth, accuracy, logical
    flow, and overall manuscript quality.
    """
    return Agent(
        role="Peer Reviewer",
        goal=(
            "Conduct a thorough peer review of the manuscript. Evaluate "
            "content depth, accuracy, logical flow, and completeness. "
            "Identify any gaps, weak arguments, or unsupported claims."
        ),
        backstory=(
            "You are a distinguished professor who has reviewed hundreds "
            "of papers for top AI conferences. You are constructive but "
            "rigorous, always providing specific, actionable feedback "
            "that helps authors improve their work significantly."
        ),
        tools=[ReadabilityScoreTool()],
        verbose=True,
        allow_delegation=False,
    )
