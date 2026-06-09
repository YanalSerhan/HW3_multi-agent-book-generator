"""Editor Agent (A-05) — Senior Copy Editor.

Reviews and improves the manuscript for clarity, consistency,
grammar, and adherence to readability standards.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.readability_tool import ReadabilityScoreTool


def create_editor_agent() -> Agent:
    """Create and return the Editor Agent.

    This agent performs comprehensive copy editing, improving prose
    quality, fixing grammatical issues, and ensuring each section
    meets the target readability score.
    """
    return Agent(
        role=AGENT_CONFIGS["editor_agent"].role,
        goal=AGENT_CONFIGS["editor_agent"].goal,
        backstory=AGENT_CONFIGS["editor_agent"].backstory,
        tools=[ReadabilityScoreTool()],
        verbose=True,
        allow_delegation=False,
    )
