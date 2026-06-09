"""Quality Assurance Agent (A-10) — Chief Quality Officer.

Performs the final quality certification, verifying all quality
gates have passed and the manuscript meets every standard.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.readability_tool import ReadabilityScoreTool


def create_qa_agent() -> Agent:
    """Create and return the Quality Assurance Agent.

    This agent serves as the final checkpoint, running all quality
    gate verifications and producing a certification report that
    confirms the manuscript is ready for publication.
    """
    return Agent(
        role=AGENT_CONFIGS["qa_agent"].role,
        goal=AGENT_CONFIGS["qa_agent"].goal,
        backstory=AGENT_CONFIGS["qa_agent"].backstory,
        tools=[ReadabilityScoreTool()],
        verbose=True,
        allow_delegation=False,
    )
