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
    cfg = AGENT_CONFIGS["pdf_production_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[LaTeXCompilerTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
