import subprocess
from pathlib import Path

from ..exceptions.domain import CompilationError
from ..shared.gatekeeper import ApiGatekeeper
from .aux_processor import post_process_aux_files
from .base import BaseClient


class LaTeXClient(BaseClient):
    """Client to execute LaTeX compilation tools via subprocess."""

    def __init__(self, gatekeeper: ApiGatekeeper | None = None) -> None:
        """Initialize."""
        # We don't necessarily rate limit local compilation, but we use the gatekeeper
        # to queue compilation tasks and enforce max_concurrent = 1.
        super().__init__("latex", gatekeeper)

    def _run_latexmk(self, tex_file: Path) -> str:
        """Run compilation using xelatex instead of latexmk to avoid Perl dependency."""
        # Clean up old auxiliary files to prevent compilation failures
        for ext in [
            ".aux",
            ".bbl",
            ".blg",
            ".fls",
            ".fdb_latexmk",
            ".log",
            ".out",
            ".toc",
            ".run.xml",
            ".glo",
            ".gls",
            ".glg",
            ".ist",
            ".idx",
            ".ind",
            ".ilg",
        ]:
            aux_file = tex_file.with_suffix(ext)
            try:
                if aux_file.exists():
                    aux_file.unlink()
            except OSError:
                pass

        cmd = ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name]
        self.logger.info(f"Running LaTeX compilation in {tex_file.parent}: {' '.join(cmd)}")

        try:
            # First pass
            res1 = subprocess.run(
                cmd, cwd=tex_file.parent, capture_output=True, text=True, timeout=90.0
            )
            if res1.returncode != 0:
                raise CompilationError(
                    "LaTeX first pass failed", {"stdout": res1.stdout, "stderr": res1.stderr}
                )

            # Post-process TOC, LOF, LOT files
            post_process_aux_files(tex_file, self.logger)

            # Bibliography pass
            import contextlib

            with contextlib.suppress(Exception):
                subprocess.run(
                    ["biber", tex_file.stem],
                    cwd=tex_file.parent,
                    capture_output=True,
                    text=True,
                    timeout=90.0,
                )

            # Glossary pass
            with contextlib.suppress(Exception):
                subprocess.run(
                    ["makeglossaries", tex_file.stem],
                    cwd=tex_file.parent,
                    capture_output=True,
                    text=True,
                    timeout=90.0,
                )

            # Index pass
            with contextlib.suppress(Exception):
                subprocess.run(
                    ["makeindex", f"{tex_file.stem}.idx"],
                    cwd=tex_file.parent,
                    capture_output=True,
                    text=True,
                    timeout=90.0,
                )

            # Second pass
            res2 = subprocess.run(
                cmd, cwd=tex_file.parent, capture_output=True, text=True, timeout=90.0
            )
            if res2.returncode != 0:
                raise CompilationError(
                    "LaTeX second pass failed", {"stdout": res2.stdout, "stderr": res2.stderr}
                )

            # Post-process TOC, LOF, LOT files before final pass
            post_process_aux_files(tex_file, self.logger)

            # Third pass for cross-references and indices
            res3 = subprocess.run(
                cmd, cwd=tex_file.parent, capture_output=True, text=True, timeout=90.0
            )
            if res3.returncode != 0:
                raise CompilationError(
                    "LaTeX third pass failed", {"stdout": res3.stdout, "stderr": res3.stderr}
                )

            # Post-process TOC, LOF, LOT files one final time to leave clean files on disk
            post_process_aux_files(tex_file, self.logger)

            return res3.stdout
        except subprocess.TimeoutExpired as e:
            raise CompilationError("LaTeX compilation timed out") from e
        except FileNotFoundError as e:
            raise CompilationError("xelatex not found. Is LaTeX installed?") from e

    def compile_pdf(self, tex_file_path: str) -> str:
        """Compile a .tex file into a PDF."""
        path = Path(tex_file_path).resolve()
        if not path.exists():
            raise CompilationError(f"Target file not found: {path}")

        return str(self._execute(self._run_latexmk, path))
