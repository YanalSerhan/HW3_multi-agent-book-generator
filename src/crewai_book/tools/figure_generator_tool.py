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
        import os
        import shutil
        import tempfile
        from pathlib import Path

        if not filename.endswith((".png", ".pdf")):
            return "FAILED: Filename must end with .png or .pdf"

        # Prevent path traversal
        if "/" in filename or "\\" in filename or filename.startswith("."):
            return "FAILED: Invalid filename. Must be a simple basename without path separators."

        # Setup output directory
        figures_dir = OUTPUT_DIR / "latex" / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        final_target_path = figures_dir / filename

        # 1. AST Sandbox: Check import allowlist, dangerous functions, and imports at top
        allowlist = {"matplotlib", "seaborn", "numpy", "pandas", "math", "random"}
        dangerous_functions = {"__import__", "exec", "eval", "compile"}
        try:
            tree = ast.parse(python_code)
        except SyntaxError as e:
            return f"FAILED: Invalid Python syntax: {e}"

        seen_non_import = False
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if seen_non_import:
                    return "FAILED: Security error. All imports must be at the top of the module."
            else:
                seen_non_import = True

        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.Import):
                for alias in ast_node.names:
                    base_module = alias.name.split(".")[0]
                    if base_module not in allowlist:
                        return f"FAILED: Security error. Importing '{alias.name}' is not allowed. Allowed modules: {', '.join(allowlist)}"
            elif isinstance(ast_node, ast.ImportFrom) and ast_node.module:
                base_module = ast_node.module.split(".")[0]
                if base_module not in allowlist:
                    return f"FAILED: Security error. Importing from '{ast_node.module}' is not allowed. Allowed modules: {', '.join(allowlist)}"
            elif (
                isinstance(ast_node, ast.Call)
                and isinstance(ast_node.func, ast.Name)
                and ast_node.func.id in dangerous_functions
            ):
                return f"FAILED: Security error. Calling '{ast_node.func.id}' is not allowed."

        # 2. Execute in isolated temp workdir
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            script_path = temp_path / f"temp_gen_{filename}.py"
            try:
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(python_code)

                # 3. Minimal subprocess env
                minimal_env = {
                    "PATH": os.environ.get("PATH", ""),
                    "MPLBACKEND": "Agg",
                    "MPLCONFIGDIR": str(temp_path),
                    "HOME": str(temp_path),
                }

                # 4. Execute with 60s timeout
                result = subprocess.run(
                    [sys.executable, script_path.name],
                    cwd=temp_path,
                    env=minimal_env,
                    capture_output=True,
                    text=True,
                    timeout=60.0,
                )

                if result.returncode != 0:
                    return (
                        "FAILED: Code execution error:\n"
                        f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
                    )

                generated_file = temp_path / filename
                if not generated_file.exists():
                    return (
                        f"FAILED: The code executed successfully but the file '{filename}' "
                        f"was not created. Make sure your code actually saves to '{filename}' "
                        "in the current working directory."
                    )

                # Move generated file to final destination
                shutil.move(str(generated_file), str(final_target_path))
                return f"SUCCESS: Figure generated and saved to {final_target_path}"

            except subprocess.TimeoutExpired:
                return "FAILED: Code execution timed out after 60 seconds."
            except Exception as e:
                return f"FAILED: Unexpected error: {e}"
