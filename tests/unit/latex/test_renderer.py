"""Unit tests for the LaTeX renderer."""

from crewai_book.domain.entities import Article, Chapter, Section
from crewai_book.latex.renderer import (
    _latex_escape,
    create_jinja_env,
    inject_provenance_footnotes,
    render_book,
)


def test_latex_escape_special_chars() -> None:
    """Escape function should handle all LaTeX special characters."""
    assert _latex_escape("price is $5") == r"price is \$5"
    assert _latex_escape("100%") == r"100\%"
    assert _latex_escape("A & B") == r"A \& B"
    assert _latex_escape("item #1") == r"item \#1"
    assert _latex_escape("under_score") == r"under\_score"


def test_inject_provenance_footnotes() -> None:
    """Test provenance footprint parsing and escaping."""
    bib_keys = {"ho2020denoising"}

    # Valid existing key
    valid_text = r"Claim [PROVENANCE: ho2020denoising | 100% $done & more | 0.95] here."
    expected_valid = r"Claim \footnote{Source: \protect\cite{ho2020denoising}. Quote: ``100\% \$done \& more''. Confidence: 0.95} here."
    assert inject_provenance_footnotes(valid_text, bib_keys) == expected_valid

    # Missing key (should fallback to simple cite)
    missing_text = r"Claim [PROVENANCE: fakekey | some quote | 0.99] here."
    expected_missing = r"Claim \protect\cite{fakekey} here."
    assert inject_provenance_footnotes(missing_text, bib_keys) == expected_missing

    # Unaffected text
    plain_text = "Just normal text."
    assert inject_provenance_footnotes(plain_text, bib_keys) == plain_text

    # Malformed tag (e.g. missing pipes or wrong format) should be stripped entirely
    malformed_text = r"Claim [PROVENANCE: missing_pipes] here. And [PROVENANCE: one | pipe] too."
    expected_malformed = r"Claim  here. And  too."
    assert inject_provenance_footnotes(malformed_text, bib_keys) == expected_malformed


def test_jinja_env_has_latex_filter() -> None:
    """Jinja2 environment should include the latex_escape filter."""
    env = create_jinja_env()
    assert "latex_escape" in env.filters


def test_render_book_produces_latex() -> None:
    """render_book should produce a compilable LaTeX document."""
    sec = Section(title="Introduction", content="Hello world.", word_count=2)
    chap = Chapter(
        number=1,
        title="Chapter One",
        chapter_summary="The first chapter.",
        sections=[sec],
    )
    article = Article(
        title="Test Book",
        authors=["Alice", "Bob"],
        abstract="An abstract.",
        target_audience="General",
        chapters=[chap],
    )

    output = render_book(article)

    assert r"\documentclass" in output
    assert "Test Book" in output
    assert r"\printbibliography" in output


def test_post_process_latex_math_protection() -> None:
    r"""post_process_latex should protect math mode from \LRE and fix nested packages."""
    from crewai_book.latex.post_processor import post_process_latex

    # Text in Hebrew environment containing English words and math blocks
    raw = r"""
\begin{hebrew}
מקסם את הלוג-סבירות \( \log p_\theta(x) \), אבל (VAEs) and (ELBO)
\end{hebrew}
"""
    # Let's run post_process_latex. It should wrap (VAEs) and (ELBO) in \LRE, but not (x) inside math mode.
    processed = post_process_latex(raw)
    assert r"\( \log p_\theta(x) \)" in processed
    assert r"\LRE{(VAEs)}" in processed
    assert r"\LRE{(ELBO)}" in processed
    assert r"\LRE{(x)}" not in processed
