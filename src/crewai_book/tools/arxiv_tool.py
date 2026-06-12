"""ArXiv academic paper search tool for CrewAI agents.

Provides access to the ArXiv API for searching academic papers,
enabling the research and citation agents to find scholarly sources.
"""

from typing import Any

import arxiv
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..observability.logger import get_logger


class ArXivSearchInput(BaseModel):
    """Input schema for the ArXiv search tool."""

    query: str = Field(..., description="The academic search query.")
    max_results: int = Field(5, description="Maximum number of papers to return.")


class ArXivTool(BaseTool):
    """Search ArXiv for academic papers on a topic.

    Queries the ArXiv API directly using the official arxiv package,
    returning structured paper metadata including titles, authors,
    abstracts, and DOIs for downstream citation processing.
    """

    name: str = "arxiv_search"
    description: str = (
        "Search ArXiv for academic papers. Returns titles, authors, "
        "abstracts, and links for scholarly research on a topic."
    )
    args_schema: type[BaseModel] = ArXivSearchInput

    def _run(self, query: str, max_results: int = 5, **kwargs: Any) -> str:
        """Execute the ArXiv search and return formatted results."""
        logger = get_logger("tools.arxiv")
        logger.info(f"Searching ArXiv for: {query}")

        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
            )
            results = list(client.results(search))
        except Exception as e:  # pragma: no cover
            logger.error(f"ArXiv search failed: {e}")  # pragma: no cover
            return f"ArXiv search failed: {e}"  # pragma: no cover

        if not results:
            return "No ArXiv papers found for the query."  # pragma: no cover

        formatted = []
        for i, paper in enumerate(results, 1):
            authors = ", ".join(a.name for a in paper.authors[:3])
            if len(paper.authors) > 3:
                authors += " et al."  # pragma: no cover
            formatted.append(
                f"{i}. {paper.title}\n"
                f"   Authors: {authors}\n"
                f"   Published: {paper.published.strftime('%Y-%m-%d')}\n"
                f"   URL: {paper.entry_id}\n"
                f"   Abstract: {paper.summary[:200]}..."
            )

        return "\n\n".join(formatted)
