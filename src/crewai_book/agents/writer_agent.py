"""Writer Agent (A-04) — Expert Technical Writer.

Produces the full manuscript text following the outline, weaving in
research sources and maintaining consistent voice and quality.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.readability_tool import ReadabilityScoreTool


def create_writer_agent() -> Agent:
    """Create and return the Writer Agent.

    This agent transforms the outline and research corpus into
    polished prose, ensuring proper citation integration and
    maintaining a consistent, authoritative voice throughout.
    Uses long-term memory to maintain consistency across chapters.
    """
    cfg = AGENT_CONFIGS["writer_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[ReadabilityScoreTool()],
        max_iter=cfg.max_iter,
        memory=True,
        verbose=True,
        allow_delegation=False,
    )
