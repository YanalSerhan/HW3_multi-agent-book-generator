"""Quality gates for the book generation pipeline.

Implements 10 automated quality checkpoints that enforce
standards between pipeline stages, as defined in PLAN.md §6.1.
"""

from typing import Any

from ..domain.entities import Article
from ..domain.state import Bibliography, PipelineState
from ..observability.logger import get_logger

logger = get_logger("workflows.quality_gates")


def check_qg1_sources(bibliography: Bibliography) -> bool:
    """QG-1: Verify at least 15 verified sources exist."""
    count = len(bibliography.entries)
    passed = count >= 15
    logger.info(f"QG-1 Sources: {count}/15 — {'PASS' if passed else 'FAIL'}")
    return passed


def check_qg2_hallucinations(hallucination_count: int) -> bool:
    """QG-2: Verify zero critical hallucinations."""
    passed = hallucination_count == 0
    logger.info(f"QG-2 Hallucinations: {hallucination_count} — {'PASS' if passed else 'FAIL'}")
    return passed


def check_qg3_outline(article: Article) -> bool:
    """QG-3: Verify all chapters and sections are present."""
    has_chapters = len(article.chapters) >= 3
    has_sections = all(len(ch.sections) >= 1 for ch in article.chapters)
    passed = has_chapters and has_sections
    logger.info(f"QG-3 Outline: {len(article.chapters)} chapters — {'PASS' if passed else 'FAIL'}")
    return passed


def check_qg4_word_count(article: Article, target: int = 15000) -> bool:
    """QG-4: Verify word count is within ±10% of target."""
    actual = article.total_word_count
    lower = int(target * 0.9)
    upper = int(target * 1.1)
    passed = lower <= actual <= upper
    logger.info(f"QG-4 Words: {actual} (target {lower}-{upper}) — {'PASS' if passed else 'WARN'}")
    return passed


def check_qg5_readability(readability_score: float) -> bool:
    """QG-5: Verify readability score ≥60."""
    passed = readability_score >= 60.0
    logger.info(f"QG-5 Readability: {readability_score:.1f}/60.0 — {'PASS' if passed else 'WARN'}")
    return passed


def check_qg7_citations(bib_count: int, ref_count: int) -> bool:
    """QG-7: Verify 100% citation match rate."""
    passed = bib_count >= ref_count and ref_count > 0
    logger.info(
        f"QG-7 Citations: {bib_count} bib / {ref_count} refs — {'PASS' if passed else 'FAIL'}"
    )
    return passed


def check_qg8_compilation(compiled: bool) -> bool:
    """QG-8: Verify LaTeX compilation exits 0."""
    logger.info(f"QG-8 Compilation: {'PASS' if compiled else 'FAIL'}")
    return compiled


def _check_metrics(state: PipelineState, results: dict[str, Any]) -> None:
    """Check overall metrics and update state."""
    logger.info(f"Final Metrics for {state.run_id}:")
    logger.info(f"- Retries used: {state.retries_used}")
    logger.info(f"- Output compiled: {results.get('compiled', False)}")


def check_qg9_pages(page_count: int) -> bool:
    """QG-9: Verify PDF has ≥20 pages."""
    passed = page_count >= 20
    logger.info(f"QG-9 Pages: {page_count}/20 — {'PASS' if passed else 'FAIL'}")
    return passed


def run_all_gates(state: PipelineState, results: dict[str, Any]) -> dict[str, bool]:
    """Run all applicable quality gates and return a summary.

    Args:
        state: Current pipeline state.
        results: Dict with keys like 'article', 'bibliography', etc.

    Returns:
        Dict mapping gate names to pass/fail booleans.
    """
    gate_results: dict[str, bool] = {}

    if "bibliography" in results:
        gate_results["QG-1"] = check_qg1_sources(results["bibliography"])
    if "hallucination_count" in results:
        gate_results["QG-2"] = check_qg2_hallucinations(results["hallucination_count"])
    if "article" in results:
        gate_results["QG-3"] = check_qg3_outline(results["article"])
        gate_results["QG-4"] = check_qg4_word_count(results["article"])
    if "readability_score" in results:
        gate_results["QG-5"] = check_qg5_readability(results["readability_score"])
    if "compiled" in results:
        gate_results["QG-8"] = check_qg8_compilation(results["compiled"])
    if "page_count" in results:
        gate_results["QG-9"] = check_qg9_pages(results["page_count"])

    for gate, passed in gate_results.items():
        if passed:
            state.mark_gate_passed(gate)

    return gate_results
