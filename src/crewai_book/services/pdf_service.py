from pathlib import Path

from ..observability.logger import get_logger
from ..sdk.latex_client import LaTeXClient


class PDFService:
    """Service to orchestrate PDF compilation."""

    def __init__(self, latex_client: LaTeXClient | None = None) -> None:
        """Initialize."""
        self.latex_client = latex_client or LaTeXClient()
        self.logger = get_logger("service.pdf")

    def build_pdf(self, source_path: Path) -> Path:
        """Compile a .tex file to PDF."""
        self.logger.info(f"Building PDF for {source_path}")

        # This executes latexmk via the SDK client
        self.latex_client.compile_pdf(str(source_path))

        expected_pdf = source_path.with_suffix(".pdf")
        if not expected_pdf.exists():
            self.logger.warning(f"Compilation succeeded but PDF not found at {expected_pdf}")

        return expected_pdf
