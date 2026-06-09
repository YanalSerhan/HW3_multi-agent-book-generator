"""Research Agent (A-01) — Senior Research Scientist.

Conducts thorough literature research using web search and ArXiv tools
to build a comprehensive corpus of verified sources on the target topic.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.arxiv_tool import ArXivTool
from ..tools.citation_validator_tool import CitationValidatorTool
from ..tools.readability_tool import ReadabilityScoreTool
from ..tools.web_search_tool import WebSearchTool


def create_research_agent() -> Agent:
    """Create and return the Research Agent.

    This agent leads the research phase, systematically searching
    academic and web sources to build a structured source corpus
    that downstream agents rely on for writing and fact-checking.
    """
    cfg = AGENT_CONFIGS["research_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[
            WebSearchTool(),
            ArXivTool(),
            CitationValidatorTool(),
            ReadabilityScoreTool(),
        ],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
