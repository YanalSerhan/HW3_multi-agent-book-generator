"""Research sub-crew for the book generation pipeline.

Orchestrates agents A-01 (Research), A-02 (Fact Verification),
and A-07 (Citation) in a hierarchical crew for the research phase.
"""

from crewai import Crew, Process, Task

from ..agents.citation_agent import create_citation_agent
from ..agents.fact_verification_agent import create_fact_verification_agent
from ..agents.research_agent import create_research_agent
from ..observability.logger import get_logger

logger = get_logger("workflows.research_crew")


def create_research_crew(topic: str) -> Crew:
    """Build and return the research sub-crew.

    This crew uses hierarchical process where the research agent
    leads, delegating fact-checking and citation tasks to the
    other agents as needed.
    """
    research_agent = create_research_agent()
    fact_agent = create_fact_verification_agent()
    citation_agent = create_citation_agent()

    research_task = Task(
        description=(
            f"Conduct comprehensive research on '{topic}'. "
            "Find at least 20 high-quality sources from academic papers "
            "and authoritative websites. Organize sources by subtopic."
        ),
        expected_output="A structured list of 20+ sources with metadata.",
        agent=research_agent,
    )

    verification_task = Task(
        description=(
            "Verify all factual claims from the research. "
            "Cross-reference each claim against at least 2 independent "
            "sources. Flag any unverified claims."
        ),
        expected_output="Verification report with confidence scores.",
        agent=fact_agent,
    )

    citation_task = Task(
        description=(
            "Validate all source citations. Check that every DOI resolves "
            "and every URL is reachable. Produce a clean bibliography."
        ),
        expected_output="Validated bibliography with BibTeX entries.",
        agent=citation_agent,
    )

    logger.info(f"Creating research crew for topic: {topic}")

    return Crew(
        agents=[research_agent, fact_agent, citation_agent],
        tasks=[research_task, verification_task, citation_task],
        process=Process.sequential,
        verbose=True,
    )
