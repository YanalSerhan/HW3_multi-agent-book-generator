"""Citation validator tool for CrewAI agents.

Validates citations by resolving DOIs and URLs to confirm
that referenced sources actually exist, preventing hallucinated citations.
"""

from typing import Any

import httpx
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..config.settings import settings
from ..observability.logger import get_logger


class CitationValidatorInput(BaseModel):
    """Input schema for the citation validator tool."""

    doi: str = Field(default="", description="DOI to validate (e.g. 10.1000/xyz123).")
    url: str = Field(default="", description="URL to validate if DOI is not available.")


class CitationValidatorTool(BaseTool):
    """Validate that a citation source actually exists.

    Checks DOIs via doi.org resolution and URLs via HTTP HEAD requests.
    Returns validation status so agents can flag hallucinated citations.
    """

    name: str = "citation_validator"
    description: str = (
        "Validate a citation by checking if its DOI resolves or URL is reachable. "
        "Provide either a DOI or URL to verify the source exists."
    )
    args_schema: type[BaseModel] = CitationValidatorInput

    def _run(self, doi: str = "", url: str = "", **kwargs: Any) -> str:
        """Validate a citation source."""
        logger = get_logger("tools.citation_validator")

        if doi:
            return self._validate_doi(doi, logger)
        if url:
            return self._validate_url(url, logger)
        return "ERROR: Provide either a DOI or URL to validate."

    @staticmethod
    def _validate_doi(doi: str, logger: Any) -> str:
        """Check if a DOI resolves via doi.org."""
        resolve_url = f"{settings.doi_resolve_url}/{doi}"
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        headers = {"User-Agent": ua}
        try:
            with httpx.Client(timeout=10.0, follow_redirects=True, headers=headers) as client:
                resp = client.head(resolve_url)
                if resp.status_code in [403, 404, 405]:
                    resp = client.get(resolve_url)
                if resp.status_code < 400:
                    return f"VALID: DOI {doi} resolves successfully."
                return f"INVALID: DOI {doi} returned status {resp.status_code}."
        except httpx.HTTPError as e:
            logger.warning(f"DOI validation failed for {doi}: {e}")
            return f"ERROR: Could not validate DOI {doi}: {e}"

    @staticmethod
    def _validate_url(url: str, logger: Any) -> str:
        """Check if a URL is reachable."""
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        headers = {"User-Agent": ua}
        try:
            with httpx.Client(timeout=10.0, follow_redirects=True, headers=headers) as client:
                resp = client.head(url)
                if resp.status_code in [403, 404, 405]:
                    resp = client.get(url)
                if resp.status_code < 400:
                    return f"VALID: URL {url} is reachable."
                return f"INVALID: URL {url} returned status {resp.status_code}."
        except httpx.HTTPError as e:
            logger.warning(f"URL validation failed for {url}: {e}")
            return f"ERROR: Could not validate URL {url}: {e}"
