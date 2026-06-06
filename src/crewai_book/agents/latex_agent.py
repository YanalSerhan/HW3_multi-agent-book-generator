"""LaTeX Formatter Agent (A-08) — Typesetting Specialist.

Converts the edited manuscript into professional LaTeX source
using the memoir class and BibLaTeX for bibliography management.
"""

from crewai import Agent

from ..tools.latex_compiler_tool import LaTeXCompilerTool


def create_latex_agent() -> Agent:
    """Create and return the LaTeX Formatter Agent.

    This agent transforms the manuscript content into compilable
    LaTeX source files using the memoir document class, ensuring
    professional typesetting with proper chapter structure.
    """
    return Agent(
        role="Typesetting Specialist",
        goal=(
            "Convert the manuscript into professional LaTeX source using "
            "the memoir class. Structure the output as a compilable book "
            "with chapters, sections, bibliography, and index."
        ),
        backstory=(
            "You are a LaTeX expert who has typeset dozens of academic "
            "books. You know the memoir class inside out and can produce "
            "beautiful, professional documents with proper typography, "
            "headers, footers, and bibliography integration."
        ),
        tools=[LaTeXCompilerTool()],
        verbose=True,
        allow_delegation=False,
    )
