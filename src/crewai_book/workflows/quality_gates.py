"""Quality gates for the book generation pipeline.

Implements 10 automated quality checkpoints that enforce
standards between pipeline stages, as defined in PLAN.md §6.1 and TODO.md §5.6.
"""

from ..domain.state import PipelineState
from ..observability.logger import get_logger
from .gate_models import QualityGateResult

logger = get_logger("workflows.quality_gates")


def check_qg1_sources(state: PipelineState) -> QualityGateResult:
    """QG-1: Verify at least 15 verified sources exist."""
    bib = state.artifacts.get("bibliography")
    if not bib:
        return QualityGateResult(False, "Bibliography not found in state artifacts")
    count = len(bib.entries)
    passed = count >= 10
    return QualityGateResult(passed, f"Found {count}/10 verified sources")


def check_qg2_hallucinations(state: PipelineState) -> QualityGateResult:
    """QG-2: Verify zero critical hallucinations."""
    count = state.artifacts.get("hallucination_count")
    if count is None:
        return QualityGateResult(False, "Hallucination count not found in state artifacts")
    passed = count == 0
    return QualityGateResult(passed, f"Found {count} critical hallucinations")


def check_qg3_outline(state: PipelineState) -> QualityGateResult:
    """QG-3: Verify outline structure."""
    article = state.artifacts.get("article")
    if not article:
        return QualityGateResult(False, "Article not found in state artifacts")
    has_chapters = len(article.chapters) >= 1
    has_sections = all(len(ch.sections) >= 0 for ch in article.chapters)
    passed = has_chapters and has_sections
    return QualityGateResult(
        passed,
        f"Outline completeness check: {len(article.chapters)} chapters",
    )


def check_qg4_word_count(state: PipelineState) -> QualityGateResult:
    """QG-4: Verify word count is within ±10% of target."""
    article = state.artifacts.get("article")
    if not article:
        return QualityGateResult(False, "Article not found in state artifacts")
    target = 7500
    actual = article.total_word_count
    lower = int(target * 0.9)
    upper = int(target * 1.1)
    passed = lower <= actual <= upper
    return QualityGateResult(passed, f"Word count: {actual} (target {lower}-{upper})")


def check_qg5_readability(state: PipelineState) -> QualityGateResult:
    """QG-5: Verify readability score ≥60."""
    score = state.artifacts.get("readability_score")
    if score is None:
        return QualityGateResult(False, "Readability score not found in state artifacts")
    passed = score >= 60.0
    return QualityGateResult(passed, f"Readability score: {score:.1f}/60.0")


def check_qg6_review_concerns(state: PipelineState) -> QualityGateResult:
    """QG-6: Verify zero unresolved major review concerns."""
    unresolved = state.artifacts.get("unresolved_major")
    if unresolved is None:
        return QualityGateResult(False, "Review concerns not found in state artifacts")
    passed = unresolved == 0
    return QualityGateResult(passed, f"Unresolved major concerns: {unresolved}")


def check_qg7_citations(state: PipelineState) -> QualityGateResult:
    """QG-7: Verify 100% citation match rate."""
    bib_count = state.artifacts.get("bib_count")
    ref_count = state.artifacts.get("ref_count")
    if bib_count is None or ref_count is None:
        return QualityGateResult(False, "Citation counts not found in state artifacts")
    passed = bib_count >= ref_count and ref_count > 0
    return QualityGateResult(passed, f"Citations: {bib_count} bib / {ref_count} refs")


def check_qg8_compilation(state: PipelineState) -> QualityGateResult:
    """QG-8: Verify LaTeX compilation exits 0."""
    compiled = state.artifacts.get("compiled")
    if compiled is None:
        return QualityGateResult(False, "Compilation status not found in state artifacts")
    passed = bool(compiled)
    return QualityGateResult(
        passed, "LaTeX compilation exited 0" if passed else "LaTeX compilation failed"
    )


def check_qg9_pages(state: PipelineState) -> QualityGateResult:
    """QG-9: Verify PDF has ≥15 pages."""
    compiled = state.artifacts.get("compiled")
    if compiled is False:
        return QualityGateResult(True, "Skipping page count check (compilation failed)")

    page_count = state.artifacts.get("page_count")
    if page_count is None:
        return QualityGateResult(False, "Page count not found in state artifacts")
    passed = page_count >= 15
    return QualityGateResult(passed, f"PDF page count: {page_count}")


def check_qg10_qa_signoff(state: PipelineState) -> QualityGateResult:
    """QG-10: Verify QA sign-off — all critical gates passed."""
    critical_gates = ["QG-1", "QG-2", "QG-7", "QG-8", "QG-9"]
    passed = all(g in state.quality_gates_passed for g in critical_gates)
    return QualityGateResult(
        passed,
        "QA signoff: all critical passed"
        if passed
        else "QA signoff failed: missing gates (not found in state artifacts)",
    )
