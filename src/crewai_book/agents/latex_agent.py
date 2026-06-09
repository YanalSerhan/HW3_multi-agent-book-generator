"""LaTeX Formatter Agent (A-08) — Typesetting Specialist.

Converts the edited manuscript into professional LaTeX source
using the memoir class and BibLaTeX for bibliography management.
"""

from crewai import Agent

from ..config.agent_configs import AGENT_CONFIGS
from ..tools.latex_compiler_tool import LaTeXCompilerTool


def create_latex_agent() -> Agent:
    """Create and return the LaTeX Formatter Agent.

    This agent transforms the manuscript content into compilable
    LaTeX source files using the memoir document class, ensuring
    professional typesetting with proper chapter structure.
    """
    cfg = AGENT_CONFIGS["latex_formatter_agent"]
    return Agent(
        role=cfg.role,
        goal=cfg.goal,
        backstory=cfg.backstory,
        tools=[LaTeXCompilerTool()],
        max_iter=cfg.max_iter,
        verbose=True,
        allow_delegation=False,
    )
