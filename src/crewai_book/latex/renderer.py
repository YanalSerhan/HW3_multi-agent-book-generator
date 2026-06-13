"""Jinja2 renderer for LaTeX templates.

Renders Article domain models into compilable LaTeX source
using Jinja2 templates with custom LaTeX-safe filters.
"""

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..domain.entities import Article
from ..observability.logger import get_logger
from .post_processor import post_process_latex

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
        "\\": r"\textbackslash{}",
    }
    return "".join(replacements.get(c, c) for c in str(text))


def inject_provenance_footnotes(text: str, bib_keys: set[str]) -> str:
    """Parse and replace PROVENANCE tags with LaTeX footnotes.

    Format: [PROVENANCE: key | short quote | confidence]
    """
    pattern = r"\[PROVENANCE:\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^\]]+?)\]"

    def replacer(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        quote = match.group(2).strip()
        conf = match.group(3).strip()

        if key in bib_keys:
            escaped_quote = _latex_escape(quote)
            return f"\\footnote{{Source: \\protect\\cite{{{key}}}. Quote: ``{escaped_quote}''. Confidence: {conf}}}"
        else:
            return f"\\protect\\cite{{{key}}}"

    text = re.sub(pattern, replacer, text)

    # Pass 2: catch hallucinated bold citations like **kingma2014autoencoding**
    def bold_replacer(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        if key in bib_keys:
            return f"\\protect\\cite{{{key}}}"
        return match.group(0)

    text = re.sub(r"\*\*([a-zA-Z0-9_\-]+)\*\*", bold_replacer, text)

    # Pass 3: catch raw standalone bib keys
    for key in bib_keys:
        # We want to match the key only if it's not already inside a \cite{}
        # A simple way is to use a negative lookbehind for {
        pattern = rf"(?<!\{{)\b{re.escape(key)}\b(?!}})"
        def repl(m: re.Match[str], k: str = key) -> str:
            return rf"\protect\cite{{{k}}}"

        text = re.sub(pattern, repl, text)

    # Pass 4: remove \LRE{} wrappers around simple math variables which break xelatex
    text = re.sub(r"\\LRE\{(\s*\(*[a-zA-Z]\)*\s*)\}", r"\1", text)

    # Cleanup pass: remove any remaining malformed PROVENANCE tags
    malformed_pattern = r"\[PROVENANCE:[^\]]*\]"

    def cleanup_replacer(match: re.Match[str]) -> str:
        malformed_tag = match.group(0)
        logger.warning(f"Stripping malformed PROVENANCE tag: {malformed_tag}")
        return ""

    return re.sub(malformed_pattern, cleanup_replacer, text)


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
        from ..config.settings import config_manager

        setup_config = config_manager.get_setup()
        cover_metadata = setup_config.get("cover_metadata", {})

        template = env.get_template("book.tex.j2")
        rendered = template.render(article=article, metadata=cover_metadata)

        rendered = post_process_latex(rendered)

        logger.info(f"Rendered LaTeX document: {len(rendered)} chars")
        return rendered
    except Exception as e:
        logger.error(f"Template rendering failed: {e}")
        raise
