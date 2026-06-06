"""Citation Agent (A-07) — Bibliographer.

Manages and validates the bibliography, ensuring all citations
are properly formatted, deduplicated, and verified.
"""

from crewai import Agent

from ..tools.arxiv_tool import ArXivTool
from ..tools.citation_validator_tool import CitationValidatorTool


def create_citation_agent() -> Agent:
    """Create and return the Citation Agent.

    This agent serves as the dedicated bibliographer, building and
    curating the .bib file with validated entries that match every
    in-text citation in the manuscript.
    """
    return Agent(
        role="Bibliographer",
        goal=(
            "Build a clean, validated bibliography. Verify every citation "
            "DOI/URL, ensure 100% match between in-text references and "
            "bibliography entries, and produce a valid .bib file."
        ),
        backstory=(
            "You are a research librarian specializing in academic citation "
            "management. You have an encyclopedic knowledge of citation "
            "styles and an obsessive attention to detail that ensures "
            "every reference is correctly formatted and verifiable."
        ),
        tools=[CitationValidatorTool(), ArXivTool()],
        verbose=True,
        allow_delegation=False,
    )
