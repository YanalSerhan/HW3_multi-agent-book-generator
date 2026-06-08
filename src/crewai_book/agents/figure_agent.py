"""Figure Generation Agent for creating visualizations."""

from crewai import Agent

from ..tools.figure_generator_tool import FigureGeneratorTool


def create_figure_agent() -> Agent:
    """Create the Figure Generation Agent.

    This agent is responsible for creating technical charts,
    diagrams, and plots using Python code execution based
    on the manuscript contents.
    """
    return Agent(
        role="Data Visualization Specialist & Illustrator",
        goal=(
            "Analyze the manuscript and create highly professional, accurate, and "
            "visually appealing technical diagrams, charts, and plots to complement the text. "
            "Save the figures as PNG or PDF files."
        ),
        backstory=(
            "A technical illustrator and data scientist who specializes in communicating complex "
            "information through clear, professional visual aids. Known for clean, academic-style "
            "figures that adhere to the highest publishing standards. Proficient in matplotlib "
            "and seaborn."
        ),
        tools=[FigureGeneratorTool()],
        verbose=True,
        allow_delegation=False,
    )
