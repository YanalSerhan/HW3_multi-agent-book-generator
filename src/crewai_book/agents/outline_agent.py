"""Outline Architect Agent (A-03) — Information Architect.

Designs the hierarchical structure of the book including chapters,
sections, and the logical flow of information through the manuscript.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS


def create_outline_agent() -> Agent:
    """Create and return the Outline Architect Agent.

    This agent designs the book's information architecture, creating
    a detailed outline that balances depth, breadth, and readability
    for the target graduate-level audience.
    """
    return Agent(
        role=AGENT_CONFIGS["outline_architect_agent"].role,
        goal=AGENT_CONFIGS["outline_architect_agent"].goal,
        backstory=AGENT_CONFIGS["outline_architect_agent"].backstory,
        tools=[],
        verbose=True,
        allow_delegation=False,
    )
