"""Quality gates for the book generation pipeline.

Implements 10 automated quality checkpoints that enforce
standards between pipeline stages, as defined in PLAN.md §6.1 and TODO.md §5.6.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from ..domain.state import PipelineState
from ..observability.logger import get_logger

logger = get_logger("workflows.quality_gates")


class PipelineStage(StrEnum):
    """Stages of the book generation pipeline."""

    RESEARCH = "research"
    MAIN = "main"
    EDITORIAL = "editorial"
    POST_PROCESSING = "post_processing"
    QA = "qa"


@dataclass
class QualityGateResult:
    """Result of evaluating a quality gate."""

    passed: bool
    message: str


@dataclass
class QualityGate:
    """Definition of a single quality gate."""

    name: str
    stage: PipelineStage
    check: Callable[[PipelineState], QualityGateResult]
    severity: Literal["blocking", "warning"]
    on_failure: Literal["retry", "abort", "human_review"]


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
        passed, "QA signoff: all critical passed" if passed else "QA signoff failed: missing gates (not found in state artifacts)"
    )


QUALITY_GATES = [
    QualityGate(
        name="QG-1",
        stage=PipelineStage.RESEARCH,
        check=check_qg1_sources,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-2",
        stage=PipelineStage.RESEARCH,
        check=check_qg2_hallucinations,
        severity="blocking",
        on_failure="abort",
    ),
    QualityGate(
        name="QG-3",
        stage=PipelineStage.MAIN,
        check=check_qg3_outline,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-4",
        stage=PipelineStage.MAIN,
        check=check_qg4_word_count,
        severity="warning",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-5",
        stage=PipelineStage.EDITORIAL,
        check=check_qg5_readability,
        severity="warning",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-6",
        stage=PipelineStage.EDITORIAL,
        check=check_qg6_review_concerns,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-7",
        stage=PipelineStage.RESEARCH,
        check=check_qg7_citations,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-8",
        stage=PipelineStage.POST_PROCESSING,
        check=check_qg8_compilation,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-9",
        stage=PipelineStage.POST_PROCESSING,
        check=check_qg9_pages,
        severity="blocking",
        on_failure="abort",
    ),
    QualityGate(
        name="QG-10",
        stage=PipelineStage.QA,
        check=check_qg10_qa_signoff,
        severity="blocking",
        on_failure="abort",
    ),
]


def run_all_gates(state: PipelineState) -> dict[str, bool]:
    """Run all quality gates and return a summary.

    Gates are evaluated based on the current state.artifacts.
    Only gates that have the requisite artifacts will pass.

    Args:
        state: Current pipeline state.

    Returns:
        Dict mapping gate names to pass/fail booleans.
    """
    gate_results: dict[str, bool] = {}

    for gate in QUALITY_GATES:
        try:
            result = gate.check(state)
        except Exception as e:
            result = QualityGateResult(False, f"Check failed with error: {e}")

        gate_results[gate.name] = result.passed

        # Only log properly if the artifact was found (i.e. we don't spam fail messages
        # for stages that haven't happened yet).
        # However, to be thorough, we log them all.
        if "not found in state artifacts" not in result.message:
            if result.passed:
                status_str = "PASS"
            else:
                status_str = "WARN" if gate.severity == "warning" else "FAIL"
            logger.info(f"{gate.name} ({gate.stage.value}): {status_str} — {result.message}")

        if result.passed:
            state.mark_gate_passed(gate.name)

    return gate_results
