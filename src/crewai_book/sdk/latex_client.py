import subprocess
from pathlib import Path

from ..exceptions.domain import CompilationError
from ..shared.gatekeeper import ApiGatekeeper
from .base import BaseClient


class LaTeXClient(BaseClient):
    """Client to execute LaTeX compilation tools via subprocess."""

    def __init__(self, gatekeeper: ApiGatekeeper | None = None) -> None:
        # We don't necessarily rate limit local compilation, but we use the gatekeeper
        # to queue compilation tasks and enforce max_concurrent = 1.
        super().__init__("latex", gatekeeper)

    def _run_latexmk(self, tex_file: Path) -> str:
        """Run latexmk on a file."""
        cmd = [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            tex_file.name
        ]

        self.logger.info(f"Running LaTeX compilation in {tex_file.parent}: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=tex_file.parent,
                capture_output=True,
                text=True,
                timeout=60.0
            )
            if result.returncode != 0:
                self.logger.error(f"Compilation failed: {result.stderr}")
                raise CompilationError("LaTeX compilation failed", {"stdout": result.stdout, "stderr": result.stderr})
            return result.stdout
        except subprocess.TimeoutExpired as e:
            raise CompilationError("LaTeX compilation timed out") from e
        except FileNotFoundError as e:
            raise CompilationError("latexmk not found. Is LaTeX installed?") from e

    def compile_pdf(self, tex_file_path: str) -> str:
        """Compile a .tex file into a PDF."""
        path = Path(tex_file_path).resolve()
        if not path.exists():
            raise CompilationError(f"Target file not found: {path}")

        return str(self._execute(self._run_latexmk, path))
