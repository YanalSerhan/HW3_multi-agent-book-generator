"""LaTeX compiler tool for CrewAI agents.

Wraps the LaTeXClient SDK to provide PDF compilation
capabilities to agents via the CrewAI BaseTool interface.
"""

from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..sdk.latex_client import LaTeXClient


class LaTeXCompilerInput(BaseModel):
    """Input schema for the LaTeX compiler tool."""

    tex_file_path: str = Field(..., description="Absolute path to the .tex file to compile.")


class LaTeXCompilerTool(BaseTool):
    """Compile a LaTeX .tex file into a PDF.

    Uses latexmk under the hood via our LaTeXClient SDK.
    Handles compilation errors and returns status messages.
    """

    name: str = "latex_compiler"
    description: str = (
        "Compile a LaTeX .tex file into a PDF document. "
        "Provide the absolute path to the .tex file."
    )
    args_schema: type[BaseModel] = LaTeXCompilerInput

    def _run(self, tex_file_path: str, **kwargs: Any) -> str:
        """Execute LaTeX compilation."""
        client = LaTeXClient()
        try:
            output = client.compile_pdf(tex_file_path)
            return f"SUCCESS: PDF compiled successfully.\n{output[:500]}"  # pragma: no cover
        except Exception as e:
            return f"FAILED: LaTeX compilation error: {e}"
