"""Reviewer Agent (A-06) — Peer Reviewer.

Performs structured peer review of the manuscript, identifying
weaknesses, gaps, and areas that need strengthening.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.readability_tool import ReadabilityScoreTool


def create_reviewer_agent() -> Agent:
    """Create and return the Reviewer Agent.

    This agent simulates an academic peer review, providing
    structured feedback on content depth, accuracy, logical
    flow, and overall manuscript quality.
    """
    return Agent(
        role=AGENT_CONFIGS["reviewer_agent"].role,
        goal=AGENT_CONFIGS["reviewer_agent"].goal,
        backstory=AGENT_CONFIGS["reviewer_agent"].backstory,
        tools=[ReadabilityScoreTool()],
        verbose=True,
        allow_delegation=False,
    )
