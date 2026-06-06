"""Web search tool for CrewAI agents.

Wraps the SearchClient SDK to provide web search capabilities
to agents via the CrewAI BaseTool interface.
"""

from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..sdk.search_client import SearchClient


class WebSearchInput(BaseModel):
    """Input schema for the web search tool."""

    query: str = Field(..., description="The search query string.")


class WebSearchTool(BaseTool):
    """Search the web for information on a topic.

    Uses the Serper API via our SearchClient SDK, which routes
    all requests through the ApiGatekeeper for rate limiting.
    """

    name: str = "web_search"
    description: str = (
        "Search the web for current information on any topic. "
        "Returns a list of relevant results with titles, links, and snippets."
    )
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str, **kwargs: Any) -> str:
        """Execute the web search and return formatted results."""
        client = SearchClient()
        results = client.search_web(query)

        if not results:
            return "No results found for the query."

        formatted = []
        for i, result in enumerate(results[:10], 1):
            title = result.get("title", "No title")
            link = result.get("link", "")
            snippet = result.get("snippet", "")
            formatted.append(f"{i}. {title}\n   URL: {link}\n   {snippet}")

        return "\n\n".join(formatted)
