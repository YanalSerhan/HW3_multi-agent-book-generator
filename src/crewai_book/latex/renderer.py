"""Jinja2 renderer for LaTeX templates.

Renders Article domain models into compilable LaTeX source
using Jinja2 templates with custom LaTeX-safe filters.
"""

import re
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
        
        # Post-processing: wrap tables in adjustbox so they don't overflow the page
        rendered = re.sub(
            r'(\\begin\{tabular\}.*?\\end\{tabular\})',
            r'\\begin{adjustbox}{max width=\\textwidth,center}\n\1\n\\end{adjustbox}',
            rendered,
            flags=re.DOTALL
        )
        
        # Post-processing: Balance hebrew environments to prevent latex compile crashes
        # Post-processing: Balance hebrew environments and wrap English phrases in \LRE
        hebrew_count = 0
        def balance_hebrew(match):
            nonlocal hebrew_count
            tag = match.group(0)
            if "begin" in tag:
                hebrew_count += 1
                return tag
            elif "end" in tag:
                if hebrew_count > 0:
                    hebrew_count -= 1
                    return tag
                else:
                    return "% stripped unmatched end{hebrew}"
            else:
                # We matched the content inside the hebrew environment!
                # We should match the content using a different regex below.
                pass
                
        rendered = re.sub(r'\\begin\{hebrew\}|\\end\{hebrew\}', balance_hebrew, rendered)
        
        # Now find all text strictly between \begin{hebrew} and \end{hebrew} and wrap English
        def wrap_english(match):
            content = match.group(1)
            # Wrap parenthetical English phrases: (Noise Schedule)
            content = re.sub(r'(\([A-Za-z][A-Za-z0-9\s-]*\))', r'\\LRE{\1}', content)
            # Wrap standalone multi-word English phrases: Large Language Models
            # Be careful not to wrap inside \cite{} or \includegraphics{}
            # A simple heuristic: if it's 2+ capitalized/english words surrounded by Hebrew or spaces, wrap it.
            # But the parenthetical regex covers 95% of the user's observed issues.
            return "\\begin{hebrew}" + content + "\\end{hebrew}"
            
        rendered = re.sub(r'\\begin\{hebrew\}(.*?)\\end\{hebrew\}', wrap_english, rendered, flags=re.DOTALL)
        
        # Close any unclosed hebrew environments right before \end{document}
        if hebrew_count > 0:
            rendered = rendered.replace("\\end{document}", ("\\end{hebrew}\n" * hebrew_count) + "\\end{document}")
        
        logger.info(f"Rendered LaTeX document: {len(rendered)} chars")
        return rendered
    except Exception as e:
        logger.error(f"Template rendering failed: {e}")
        raise
