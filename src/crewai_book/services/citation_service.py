from ..domain.state import Bibliography
from ..observability.logger import get_logger


class CitationService:
    """Service to handle citation validation and formatting."""

    def __init__(self) -> None:
        """Initialize."""
        self.logger = get_logger("service.citation")

    def generate_bibtex(self, bibliography: Bibliography) -> str:
        """Generate BibTeX string from Bibliography object."""
        lines = []
        for cit in bibliography.entries:
            authors_str = " and ".join(cit.authors)
            lines.append(f"@article{{{cit.bibtex_key},")
            lines.append(f"  title={{{cit.title}}},")
            lines.append(f"  author={{{authors_str}}},")
            lines.append(f"  year={{{cit.year}}},")
            if cit.venue:
                lines.append(f"  journal={{{cit.venue}}},")
            if cit.doi:
                lines.append(f"  doi={{{cit.doi}}},")
            if cit.url:
                lines.append(f"  url={{{cit.url}}},")
            lines.append("}")
            lines.append("")

        return "\n".join(lines)
