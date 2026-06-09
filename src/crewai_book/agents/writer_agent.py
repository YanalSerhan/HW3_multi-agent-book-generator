"""Writer Agent (A-04) — Expert Technical Writer.

Produces the full manuscript text following the outline, weaving in
research sources and maintaining consistent voice and quality.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.web_search_tool import WebSearchTool


def create_writer_agent() -> Agent:
    """Create and return the Writer Agent.

    This agent transforms the outline and research corpus into
    polished prose, ensuring proper citation integration and
    maintaining a consistent, authoritative voice throughout.
    """
    return Agent(
        role=AGENT_CONFIGS["writer_agent"].role,
        goal=AGENT_CONFIGS["writer_agent"].goal,
        backstory=AGENT_CONFIGS["writer_agent"].backstory,
        tools=[WebSearchTool()],
        verbose=True,
        allow_delegation=False,
    )
