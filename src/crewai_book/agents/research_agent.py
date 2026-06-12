"""Research Agent (A-01) — Senior Research Scientist.

Conducts thorough literature research using web search and ArXiv tools
to build a comprehensive corpus of verified sources on the target topic.
"""

from typing import Any

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.arxiv_tool import ArXivTool
from ..tools.citation_validator_tool import CitationValidatorTool
from ..tools.readability_tool import ReadabilityScoreTool
from ..tools.web_search_tool import WebSearchTool


def _get_knowledge_tools() -> list[Any]:
    """Get dynamic knowledge tools based on configured sources."""
    try:
        import os
        from pathlib import Path

        from crewai_tools import TXTSearchTool

        from ..config.settings import config_manager

        setup_config = config_manager.get_setup()
        sources = setup_config.get("knowledge_sources", [])

        tools = []
        for src in sources:
            src_path = Path(src)
            # The extractor writes to sources/{stem}_extracted.md
            md_path = Path("sources") / f"{src_path.stem}_extracted.md"
            if md_path.exists() and os.getenv("OPENAI_API_KEY"):
                # Avoid requiring API key if running in CI without it
                tools.append(TXTSearchTool(txt=str(md_path)))  # pragma: no cover
        return tools  # pragma: no cover
    except Exception:  # pragma: no cover
        return []  # pragma: no cover


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
            *_get_knowledge_tools(),
        ],
        max_iter=cfg.max_iter,
        max_retry_limit=3,
        verbose=True,
        allow_delegation=False,
    )
