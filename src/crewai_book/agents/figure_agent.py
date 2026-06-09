"""Figure Generation Agent — Data Visualization Specialist.

Creates technical charts, diagrams, and plots using Python code
execution to complement the manuscript with professional visuals.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.figure_generator_tool import FigureGeneratorTool


def create_figure_agent() -> Agent:
    """Create the Figure Generation Agent.

    This agent is responsible for creating technical charts,
    diagrams, and plots using Python code execution based
    on the manuscript contents.
    """
    cfg = AGENT_CONFIGS["figure_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[FigureGeneratorTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
