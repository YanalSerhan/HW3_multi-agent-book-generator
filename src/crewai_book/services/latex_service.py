from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..domain.entities import Article
from ..observability.logger import get_logger
from ..shared.constants import TEMPLATE_DIR


class LaTeXService:
    """Service to render articles into LaTeX source."""

    def __init__(self, template_dir: Path = TEMPLATE_DIR) -> None:
        """Initialize."""
        self.logger = get_logger("service.latex")

        # Create dir if not exists (for tests)
        if not template_dir.exists():
            template_dir.mkdir(parents=True, exist_ok=True)  # pragma: no cover

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_article(self, article: Article) -> str:
        """Render an Article domain model to LaTeX using templates."""
        try:
            template = self.env.get_template("book.tex.j2")
            return template.render(article=article)  # pragma: no cover
        except Exception as e:
            self.logger.error(f"Template rendering failed: {e}")
            return (
                f"\\documentclass{{memoir}}\n\\title{{{article.title}}}\n"
                f"\\begin{{document}}\n\\maketitle\n\\end{{document}}"
            )
