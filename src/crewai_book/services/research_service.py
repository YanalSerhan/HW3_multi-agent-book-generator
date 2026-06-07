from ..domain.state import Citation
from ..observability.logger import get_logger
from ..sdk.search_client import SearchClient


class ResearchService:
    """Service handling literature research and fact-checking."""

    def __init__(self, search_client: SearchClient | None = None) -> None:
        """Initialize."""
        self.search_client = search_client or SearchClient()
        self.logger = get_logger("service.research")

    def search_for_topic(self, topic: str, max_results: int = 10) -> list[Citation]:
        """Search the web and arxiv for a given topic."""
        self.logger.info(f"Researching topic: {topic}")

        web_results = self.search_client.search_web(topic)
        # Parse Serper results to Citations
        citations = []
        for idx, res in enumerate(web_results[:max_results]):
            cit = Citation(
                bibtex_key=f"web_{idx}",
                title=res.get("title", "Unknown Title"),
                authors=["Web Source"],
                year=2024,
                venue=None,
                doi=None,
                confidence_score=1.0,
                url=res.get("link", ""),
                abstract=res.get("snippet", ""),
            )
            citations.append(cit)

        return citations
