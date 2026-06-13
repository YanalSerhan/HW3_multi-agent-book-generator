from typing import Any

import httpx

from ..config.settings import settings
from ..exceptions.domain import SearchError
from ..shared.gatekeeper import ApiGatekeeper
from .base import BaseClient


class SearchClient(BaseClient):
    """Client for web and academic search APIs."""

    def __init__(self, gatekeeper: ApiGatekeeper | None = None) -> None:
        """Initialize."""
        super().__init__("serper", gatekeeper)
        self.headers = {
            "X-API-KEY": settings.serper_api_key.get_secret_value(),
            "Content-Type": "application/json",
        }

    def _do_search(self, query: str) -> dict[str, Any]:
        """Perform a search query via Serper."""
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.post(
                    settings.serper_api_url,
                    json={"q": query, "num": 10},
                    headers=self.headers,
                )
                response.raise_for_status()
                data = response.json()
                return data if isinstance(data, dict) else {}
        except httpx.HTTPError as e:
            self.logger.error(f"Search API failed for query '{query}': {e}")
            raise SearchError(f"Search failed: {query}", {"error": str(e)}) from e

    def search_web(self, query: str) -> list[dict[str, Any]]:
        """Search the web and return results."""
        if not settings.serper_api_key.get_secret_value():
            self.logger.warning("Serper API key not configured. Returning empty results.")
            return []

        data = self._execute(self._do_search, query)
        if isinstance(data, dict):
            organic = data.get("organic", [])
            if isinstance(organic, list):
                return organic
        return []

    def search_arxiv(self, query: str) -> list[dict[str, Any]]:
        """Mock arxiv search endpoint utilizing the arxiv service rate limits."""
        # Here we just use a generic gatekeeper for Arxiv
        # Real implementation would use the `arxiv` python package.
        self.logger.info(f"Simulating ArXiv search for: {query}")
        return []
