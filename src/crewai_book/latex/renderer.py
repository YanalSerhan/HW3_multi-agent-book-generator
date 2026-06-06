"""Jinja2 renderer for LaTeX templates.

Renders Article domain models into compilable LaTeX source
using Jinja2 templates with custom LaTeX-safe filters.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..domain.entities import Article
from ..observability.logger import get_logger

logger = get_logger("latex.renderer")

# Default template directory inside this package
_DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"


def _latex_escape(text: str) -> str:
    """Escape special LaTeX characters in text.

    Handles the 10 LaTeX special characters to prevent
    compilation errors from user-generated content.
    """
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    return text


def create_jinja_env(template_dir: Path | None = None) -> Environment:
    """Create a Jinja2 environment configured for LaTeX rendering.

    Args:
        template_dir: Path to template directory. Defaults to
            the bundled templates directory.

    Returns:
        Configured Jinja2 Environment with LaTeX-safe filters.
    """
    tpl_dir = template_dir or _DEFAULT_TEMPLATE_DIR

    env = Environment(
        loader=FileSystemLoader(str(tpl_dir)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="{{",
        variable_end_string="}}",
        comment_start_string="{#",
        comment_end_string="#}",
    )

    env.filters["latex_escape"] = _latex_escape

    return env


def render_book(article: Article, template_dir: Path | None = None) -> str:
    """Render an Article into a complete LaTeX document.

    Args:
        article: The Article domain model to render.
        template_dir: Optional override for template location.

    Returns:
        The rendered LaTeX source as a string.
    """
    env = create_jinja_env(template_dir)

    try:
        template = env.get_template("book.tex.j2")
        rendered = template.render(article=article)
        logger.info(f"Rendered LaTeX document: {len(rendered)} chars")
        return rendered
    except Exception as e:
        logger.error(f"Template rendering failed: {e}")
        raise
