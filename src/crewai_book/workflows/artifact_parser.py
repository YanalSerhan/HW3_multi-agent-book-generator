"""Utilities to parse raw text artifacts into domain models."""

import re
from pathlib import Path

from ..domain.entities import Article, Chapter, Section
from ..domain.state import Bibliography, Citation
from ..observability.logger import get_logger

logger = get_logger("workflows.artifact_parser")


def parse_bibliography(filepath: Path) -> Bibliography:
    """Parse a BibTeX file into a Bibliography object."""
    bib = Bibliography()
    if not filepath.exists():
        logger.warning(f"Bibliography file not found: {filepath}")
        return bib

    content = filepath.read_text(encoding="utf-8")

    # Strip markdown code fences that LLMs sometimes wrap BibTeX in
    content = re.sub(r"```(?:bibtex|bib|latex)?\s*\n?", "", content)
    content = content.replace("```", "")

    # Simple regex to count entries and extract keys
    # Matches @article{key, @book{key, etc.
    entry_pattern = re.compile(r"@\w+\s*\{\s*([^,]+),", re.IGNORECASE)

    matches = entry_pattern.findall(content)

    if not matches and content.strip():
        logger.error(
            f"Bibliography file exists ({len(content)} bytes) but contains "
            f"no parseable BibTeX entries. Agent likely output non-BibTeX text. "
            f"First 100 chars: {content[:100]!r}"
        )

    for i, key in enumerate(matches):
        cit = Citation(
            bibtex_key=key.strip(),
            title=f"Parsed Title {i}",
            authors=["Parsed Author"],
            year=2024,
        )
        bib.add_citation(cit)

    return bib


def parse_hallucination_count(filepath: Path) -> int:
    """Scan verification report for unverified claims or hallucinations."""
    if not filepath.exists():
        logger.warning(f"Verification report not found: {filepath}")
        return 0

    content = filepath.read_text(encoding="utf-8")

    # Often agents return "0 hallucinations" or "no hallucinations" when none are found.
    content_lower = content.lower()
    if "0 hallucinations" in content_lower or "no hallucinations" in content_lower:
        return 0

    # Count occurrences of red-flag words
    flags = (
        content_lower.count("hallucination")
        + content_lower.count("unverified")
        + content_lower.count("false claim")
    )

    return flags


def parse_article(filepath: Path) -> Article:
    """Naively parse markdown manuscript into Article entity for checks."""
    if not filepath.exists():
        logger.warning(f"Manuscript not found: {filepath}")
        return Article(title="Unknown", authors=[], abstract="", target_audience="", chapters=[])

    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    chapters: list[Chapter] = []
    current_chapter: Chapter | None = None
    current_section: Section | None = None

    # Simple state machine to parse markdown or latex headers
    for line in lines:
        if line.startswith("# ") or line.startswith("\\chapter{"):
            # New chapter
            if current_chapter and current_section:
                current_section.update_word_count()
            if current_chapter:
                chapters.append(current_chapter)

            title = line.lstrip("# ").replace("\\chapter{", "").rstrip("}")
            current_chapter = Chapter(
                number=len(chapters) + 1,
                title=title.strip(),
                chapter_summary="",
                sections=[],
            )
            current_section = None

        elif (
            line.startswith("## ")
            or line.startswith("### ")
            or line.startswith("\\section{")
            or line.startswith("\\subsection{")
        ):
            # New section
            if current_section:
                current_section.update_word_count()

            if not current_chapter:
                current_chapter = Chapter(
                    number=1, title="Default", chapter_summary="", sections=[]
                )

            title = (
                line.lstrip("# ")
                .replace("\\section{", "")
                .replace("\\subsection{", "")
                .rstrip("}")
            )
            current_section = Section(title=title.strip(), content="")
            current_chapter.sections.append(current_section)

        else:
            # Body text
            if current_section:
                current_section.content += line + "\n"
            elif current_chapter:
                # Text before any section
                if not current_chapter.sections:
                    current_section = Section(title="Introduction", content="")
                    current_chapter.sections.append(current_section)
                current_chapter.sections[-1].content += line + "\n"

    if current_section:
        current_section.update_word_count()
    if current_chapter:
        chapters.append(current_chapter)

    art = Article(
        title="Parsed Article", authors=[], abstract="", target_audience="", chapters=chapters
    )
    return art
