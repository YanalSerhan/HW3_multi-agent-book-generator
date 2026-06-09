"""Research Agent (A-01) — Senior Research Scientist.

Conducts thorough literature research using web search and ArXiv tools
to build a comprehensive corpus of verified sources on the target topic.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.arxiv_tool import ArXivTool
from ..tools.web_search_tool import WebSearchTool


def create_research_agent() -> Agent:
    """Create and return the Research Agent.

    This agent leads the research phase, systematically searching
    academic and web sources to build a structured source corpus
    that downstream agents rely on for writing and fact-checking.
    """
    return Agent(
        role=AGENT_CONFIGS["research_agent"].role,
        goal=AGENT_CONFIGS["research_agent"].goal,
        backstory=AGENT_CONFIGS["research_agent"].backstory,
        tools=[WebSearchTool(), ArXivTool()],
        verbose=True,
        allow_delegation=False,
    )
