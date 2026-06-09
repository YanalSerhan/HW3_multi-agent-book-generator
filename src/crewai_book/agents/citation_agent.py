"""Citation Agent (A-07) — Bibliographer.

Manages and validates the bibliography, ensuring all citations
are properly formatted, deduplicated, and verified.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.arxiv_tool import ArXivTool
from ..tools.citation_validator_tool import CitationValidatorTool


def create_citation_agent() -> Agent:
    """Create and return the Citation Agent.

    This agent serves as the dedicated bibliographer, building and
    curating the .bib file with validated entries that match every
    in-text citation in the manuscript.
    """
    return Agent(
        role=AGENT_CONFIGS["citation_agent"].role,
        goal=AGENT_CONFIGS["citation_agent"].goal,
        backstory=AGENT_CONFIGS["citation_agent"].backstory,
        tools=[CitationValidatorTool(), ArXivTool()],
        verbose=True,
        allow_delegation=False,
    )
