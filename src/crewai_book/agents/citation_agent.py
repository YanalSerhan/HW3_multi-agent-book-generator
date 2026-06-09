"""Citation Agent (A-07) — Bibliographer.

Manages and validates the bibliography, ensuring all citations
are properly formatted, deduplicated, and verified.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.arxiv_tool import ArXivTool
from ..tools.citation_validator_tool import CitationValidatorTool
from ..tools.web_search_tool import WebSearchTool


def create_citation_agent() -> Agent:
    """Create and return the Citation Agent.

    This agent serves as the dedicated bibliographer, building and
    curating the .bib file with validated entries that match every
    in-text citation in the manuscript.
    """
    cfg = AGENT_CONFIGS["citation_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[CitationValidatorTool(), WebSearchTool(), ArXivTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
