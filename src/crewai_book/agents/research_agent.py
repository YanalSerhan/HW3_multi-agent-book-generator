"""Research Agent (A-01) — Senior Research Scientist.

Conducts thorough literature research using web search and ArXiv tools
to build a comprehensive corpus of verified sources on the target topic.
"""

from crewai import Agent

from ..tools.arxiv_tool import ArXivTool
from ..tools.web_search_tool import WebSearchTool


def create_research_agent() -> Agent:
    """Create and return the Research Agent.

    This agent leads the research phase, systematically searching
    academic and web sources to build a structured source corpus
    that downstream agents rely on for writing and fact-checking.
    """
    return Agent(
        role="Senior Research Scientist",
        goal=(
            "Conduct exhaustive research on the assigned topic, identifying "
            "at least 20 high-quality sources from academic papers, textbooks, "
            "and authoritative web resources."
        ),
        backstory=(
            "You are a seasoned research scientist with 15 years of experience "
            "in AI and multi-agent systems. You have published in top venues "
            "and know how to distinguish credible sources from unreliable ones. "
            "You systematically categorize sources by relevance and quality."
        ),
        tools=[WebSearchTool(), ArXivTool()],
        verbose=True,
        allow_delegation=False,
    )
