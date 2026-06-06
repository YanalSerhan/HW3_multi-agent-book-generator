"""Fact Verification Agent (A-02) — Critical Fact Checker.

Cross-verifies claims made in the manuscript against independent sources
to detect and flag potential hallucinations before publication.
"""

from crewai import Agent

from ..tools.fact_check_tool import FactCheckTool
from ..tools.web_search_tool import WebSearchTool


def create_fact_verification_agent() -> Agent:
    """Create and return the Fact Verification Agent.

    This agent acts as a critical gatekeeper, ensuring every factual
    claim in the manuscript is backed by at least two independent
    sources, with zero tolerance for hallucinated content.
    """
    return Agent(
        role="Critical Fact Checker",
        goal=(
            "Verify every factual claim in the manuscript against "
            "independent sources. Flag any claim with fewer than 2 "
            "corroborating sources as potentially hallucinated."
        ),
        backstory=(
            "You are an investigative journalist turned AI safety researcher. "
            "You have a reputation for catching fabricated claims that slip "
            "past other reviewers. You are methodical and skeptical, never "
            "accepting a claim at face value without verification."
        ),
        tools=[FactCheckTool(), WebSearchTool()],
        verbose=True,
        allow_delegation=False,
    )
