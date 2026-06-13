# pyrefly: ignore [missing-import]
from pathlib import Path

from crewai_book.workflows.artifact_parser import (
    parse_article,
    parse_bibliography,
    parse_hallucination_count,
)


def test_parse_bibliography_valid(tmp_path: Path) -> None:
    bib_file = tmp_path / "valid.bib"
    content = """
@article{test1, title={Test 1}}
@book{test2, author={Test 2}}
    """
    bib_file.write_text(content)

    bib = parse_bibliography(bib_file)
    assert len(bib.entries) == 2
    assert bib.entries[0].bibtex_key == "test1"
    assert bib.entries[1].bibtex_key == "test2"

def test_parse_bibliography_markdown_wrapped(tmp_path: Path) -> None:
    bib_file = tmp_path / "wrapped.bib"
    content = """```bibtex
@article{test3, title={Test 3}}
```"""
    bib_file.write_text(content)

    bib = parse_bibliography(bib_file)
    assert len(bib.entries) == 1
    assert bib.entries[0].bibtex_key == "test3"

def test_parse_bibliography_missing(tmp_path: Path) -> None:
    bib_file = tmp_path / "missing.bib"
    bib = parse_bibliography(bib_file)
    assert len(bib.entries) == 0

def test_parse_bibliography_malformed(tmp_path: Path) -> None:
    bib_file = tmp_path / "malformed.bib"
    bib_file.write_text("This is just some random text without any bibtex entries.")

    bib = parse_bibliography(bib_file)
    assert len(bib.entries) == 0

def test_parse_hallucination_count_zero(tmp_path: Path) -> None:
    rep_file = tmp_path / "report.md"
    rep_file.write_text("I found 0 hallucinations in the text.")
    assert parse_hallucination_count(rep_file) == 0

def test_parse_hallucination_count_no_hallucinations(tmp_path: Path) -> None:
    rep_file = tmp_path / "report.md"
    rep_file.write_text("There are no hallucinations here.")
    assert parse_hallucination_count(rep_file) == 0

def test_parse_hallucination_count_flags(tmp_path: Path) -> None:
    rep_file = tmp_path / "report.md"
    rep_file.write_text("This is an unverified claim. And another hallucination. A false claim!")
    assert parse_hallucination_count(rep_file) == 3

def test_parse_hallucination_count_missing(tmp_path: Path) -> None:
    rep_file = tmp_path / "missing.md"
    assert parse_hallucination_count(rep_file) == 0

def test_parse_article_markdown(tmp_path: Path) -> None:
    art_file = tmp_path / "article.md"
    content = """# Chapter 1
## Section 1
Hello world.
## Section 2
More text.
# Chapter 2
### Section 1
Final text."""
    art_file.write_text(content)

    art = parse_article(art_file)
    assert len(art.chapters) == 2
    assert art.chapters[0].title == "Chapter 1"
    assert len(art.chapters[0].sections) == 2
    assert art.chapters[0].sections[0].title == "Section 1"
    assert art.chapters[0].sections[0].content == "Hello world.\n"
    assert art.chapters[0].sections[1].title == "Section 2"
    assert art.chapters[1].title == "Chapter 2"
    assert len(art.chapters[1].sections) == 1

def test_parse_article_latex(tmp_path: Path) -> None:
    art_file = tmp_path / "article.tex"
    content = """\\chapter{Intro}
\\section{Background}
Latex text.
\\subsection{Deep dive}
More text."""
    art_file.write_text(content)

    art = parse_article(art_file)
    assert len(art.chapters) == 1
    assert art.chapters[0].title == "Intro"
    assert len(art.chapters[0].sections) == 2
    assert art.chapters[0].sections[0].title == "Background"
    assert art.chapters[0].sections[1].title == "Deep dive"

def test_parse_article_no_chapter(tmp_path: Path) -> None:
    art_file = tmp_path / "article.md"
    content = """## Section Only
Text here."""
    art_file.write_text(content)

    art = parse_article(art_file)
    assert len(art.chapters) == 1
    assert art.chapters[0].title == "Default"
    assert len(art.chapters[0].sections) == 1

def test_parse_article_no_section(tmp_path: Path) -> None:
    art_file = tmp_path / "article.md"
    content = """# Chapter Only
Text here."""
    art_file.write_text(content)

    art = parse_article(art_file)
    assert len(art.chapters) == 1
    assert len(art.chapters[0].sections) == 1
    assert art.chapters[0].sections[0].title == "Introduction"

def test_parse_article_missing(tmp_path: Path) -> None:
    art_file = tmp_path / "missing.md"
    art = parse_article(art_file)
    assert art.title == "Unknown"
