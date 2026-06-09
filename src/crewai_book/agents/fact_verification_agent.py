"""Fact Verification Agent (A-02) — Critical Fact Checker.

Cross-verifies claims made in the manuscript against independent sources
to detect and flag potential hallucinations before publication.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.citation_validator_tool import CitationValidatorTool
from ..tools.fact_check_tool import FactCheckTool
from ..tools.web_search_tool import WebSearchTool


def create_fact_verification_agent() -> Agent:
    """Create and return the Fact Verification Agent.

    This agent acts as a critical gatekeeper, ensuring every factual
    claim in the manuscript is backed by at least two independent
    sources, with zero tolerance for hallucinated content.
    """
    cfg = AGENT_CONFIGS["fact_verification_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[WebSearchTool(), CitationValidatorTool(), FactCheckTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
