"""Figure Generation Tool for creating plots and diagrams via Python."""

import ast
import subprocess
import sys
from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..shared.constants import OUTPUT_DIR


class FigureGeneratorInput(BaseModel):
    """Input schema for the Figure Generator tool."""

    python_code: str = Field(
        ...,
        description=(
            "The complete Python code to generate the figure. Must use matplotlib "
            "or seaborn. The code MUST save the figure to the filename specified "
            "in the 'filename' argument, and NOT show the plot interactively. "
            "Do not include plt.show()."
        ),
    )
    filename: str = Field(
        ...,
        description=(
            "The target filename for the figure (e.g., 'architecture.png'). "
            "Must end in .png or .pdf."
        ),
    )


class FigureGeneratorTool(BaseTool):
    """Execute Python code to generate figures and save them to the output directory."""

    name: str = "figure_generator"
    description: str = (
        "Execute Python code to generate figures, plots, or diagrams. "
        "Provide complete, runnable Python code using matplotlib or seaborn, "
        "and specify the target filename. The tool will save the generated "
        "image and return the absolute path to the saved file."
    )
    args_schema: type[BaseModel] = FigureGeneratorInput

    def _run(self, python_code: str, filename: str, **kwargs: Any) -> str:
        """Execute the python code to generate the figure."""
        if not filename.endswith((".png", ".pdf")):
            return "FAILED: Filename must end with .png or .pdf"

        # Setup output directory
        figures_dir = OUTPUT_DIR / "latex" / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        target_path = figures_dir / filename

        # Inject the correct save path into the code
        # We replace the filename in the code with the absolute target path
        # To be safe, we just tell the script to save to the current working directory
        # and we set cwd to the figures directory.

        # Verify the code is valid Python syntax
        try:
            ast.parse(python_code)
        except SyntaxError as e:
            return f"FAILED: Invalid Python syntax: {e}"

        # Write code to a temporary script
        script_path = figures_dir / f"temp_gen_{filename}.py"
        try:
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(python_code)

            # Execute the script
            result = subprocess.run(
                [sys.executable, script_path.name],
                cwd=figures_dir,
                capture_output=True,
                text=True,
                timeout=30.0,
            )

            if result.returncode != 0:
                return (
                    "FAILED: Code execution error:\n"
                    f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
                )

            if not target_path.exists():
                return (
                    f"FAILED: The code executed successfully but the file '{filename}' "
                    f"was not created. Make sure your code actually saves to '{filename}'."
                )

            return f"SUCCESS: Figure generated and saved to {target_path}"
        except subprocess.TimeoutExpired:
            return "FAILED: Code execution timed out after 30 seconds."
        except Exception as e:
            return f"FAILED: Unexpected error: {e}"
        finally:
            if script_path.exists():
                script_path.unlink()
