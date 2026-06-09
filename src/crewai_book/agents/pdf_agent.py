"""PDF Production Agent (A-09) — Production QC Specialist.

Handles the final PDF compilation, verifying that the LaTeX
source compiles cleanly and the output meets quality standards.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.latex_compiler_tool import LaTeXCompilerTool


def create_pdf_agent() -> Agent:
    """Create and return the PDF Production Agent.

    This agent manages the compilation pipeline, running latexmk
    to produce the final PDF and verifying page count, rendering
    quality, and that all elements (figures, bibliography) appear.
    """
    return Agent(
        role=AGENT_CONFIGS["pdf_production_agent"].role,
        goal=AGENT_CONFIGS["pdf_production_agent"].goal,
        backstory=AGENT_CONFIGS["pdf_production_agent"].backstory,
        tools=[LaTeXCompilerTool()],
        verbose=True,
        allow_delegation=False,
    )
