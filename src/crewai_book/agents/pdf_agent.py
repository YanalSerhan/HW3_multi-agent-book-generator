"""PDF Production Agent (A-09) — Production QC Specialist.

Handles the final PDF compilation, verifying that the LaTeX
source compiles cleanly and the output meets quality standards.
"""

from crewai import Agent

from ..tools.latex_compiler_tool import LaTeXCompilerTool


def create_pdf_agent() -> Agent:
    """Create and return the PDF Production Agent.

    This agent manages the compilation pipeline, running latexmk
    to produce the final PDF and verifying page count, rendering
    quality, and that all elements (figures, bibliography) appear.
    """
    return Agent(
        role="Production QC Specialist",
        goal=(
            "Compile the LaTeX source into a final PDF. Verify the PDF "
            "has ≥20 pages, all chapters render correctly, the bibliography "
            "appears, and there are no compilation warnings."
        ),
        backstory=(
            "You are a production manager at an academic publishing house. "
            "You have overseen the production of thousands of books and "
            "know every LaTeX compilation pitfall. You catch rendering "
            "issues that others miss and ensure pixel-perfect output."
        ),
        tools=[LaTeXCompilerTool()],
        verbose=True,
        allow_delegation=False,
    )
