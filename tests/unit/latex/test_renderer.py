"""Unit tests for the LaTeX renderer."""

from crewai_book.domain.entities import Article, Chapter, Section
from crewai_book.latex.renderer import _latex_escape, create_jinja_env, render_book


def test_latex_escape_special_chars() -> None:
    """Escape function should handle all LaTeX special characters."""
    assert _latex_escape("price is $5") == r"price is \$5"
    assert _latex_escape("100%") == r"100\%"
    assert _latex_escape("A & B") == r"A \& B"
    assert _latex_escape("item #1") == r"item \#1"
    assert _latex_escape("under_score") == r"under\_score"


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
    assert "Chapter One" in output
    assert "Introduction" in output
    assert "Hello world." in output
    assert r"\printbibliography" in output
