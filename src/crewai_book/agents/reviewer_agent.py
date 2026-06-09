"""Reviewer Agent (A-06) — Peer Reviewer.

Performs structured peer review of the manuscript, identifying
weaknesses, gaps, and areas that need strengthening.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.citation_validator_tool import CitationValidatorTool
from ..tools.fact_check_tool import FactCheckTool


def create_reviewer_agent() -> Agent:
    """Create and return the Reviewer Agent.

    This agent simulates an academic peer review, providing
    structured feedback on content depth, accuracy, logical
    flow, and overall manuscript quality.
    """
    cfg = AGENT_CONFIGS["reviewer_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[CitationValidatorTool(), FactCheckTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
