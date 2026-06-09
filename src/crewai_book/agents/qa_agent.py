"""Quality Assurance Agent (A-10) — Chief Quality Officer.

Performs the final quality certification, verifying all quality
gates have passed and the manuscript meets every standard.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.citation_validator_tool import CitationValidatorTool
from ..tools.readability_tool import ReadabilityScoreTool


def create_qa_agent() -> Agent:
    """Create and return the Quality Assurance Agent.

    This agent serves as the final checkpoint, running all quality
    gate verifications and producing a certification report that
    confirms the manuscript is ready for publication.
    """
    cfg = AGENT_CONFIGS["qa_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[ReadabilityScoreTool(), CitationValidatorTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
