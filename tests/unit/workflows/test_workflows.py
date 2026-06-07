"""Unit tests for workflow components."""

from unittest.mock import MagicMock, patch

import pytest

from crewai_book.domain.entities import Article, Chapter, Section
from crewai_book.domain.state import Bibliography, Citation, PipelineState
from crewai_book.workflows.quality_gates import (
    check_qg1_sources,
    check_qg2_hallucinations,
    check_qg3_outline,
    check_qg5_readability,
    check_qg9_pages,
    run_all_gates,
)
from crewai_book.workflows.retry_handler import retry_with_backoff


def test_retry_succeeds_first_try() -> None:
    """Retry handler should return immediately on success."""
    result = retry_with_backoff(lambda: "ok", max_retries=3)
    assert result == "ok"


@patch("crewai_book.workflows.retry_handler.time.sleep")
def test_retry_succeeds_after_failures(mock_sleep: MagicMock) -> None:
    """Retry handler should succeed after transient failures."""
    call_count = {"n": 0}

    def flaky() -> str:
        """Test docstring."""
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise ValueError("transient")
        return "recovered"

    result = retry_with_backoff(flaky, max_retries=3, base_delay=0.01)
    assert result == "recovered"
    assert mock_sleep.call_count == 2


@patch("crewai_book.workflows.retry_handler.time.sleep")
def test_retry_exhausted(mock_sleep: MagicMock) -> None:
    """Retry handler should raise after exhausting all attempts."""
    with pytest.raises(ValueError, match="permanent"):
        retry_with_backoff(
            lambda: (_ for _ in ()).throw(ValueError("permanent")),
            max_retries=1,
            base_delay=0.01,
        )


def _make_bibliography(n: int) -> Bibliography:
    """Helper to create a bibliography with n entries."""
    bib = Bibliography()
    for i in range(n):
        bib.add_citation(
            Citation(
                bibtex_key=f"key{i}",
                title=f"Paper {i}",
                authors=["Author"],
                year=2024,
            )
        )
    return bib


def test_qg1_sources_pass() -> None:
    """QG-1 should pass with ≥15 sources."""
    assert check_qg1_sources(_make_bibliography(15)) is True


def test_qg1_sources_fail() -> None:
    """QG-1 should fail with <15 sources."""
    assert check_qg1_sources(_make_bibliography(5)) is False


def test_qg2_hallucinations() -> None:
    """QG-2 should pass with 0 hallucinations."""
    assert check_qg2_hallucinations(0) is True
    assert check_qg2_hallucinations(1) is False


def test_qg3_outline() -> None:
    """QG-3 should verify chapters and sections."""
    sec = Section(title="S", content="text", word_count=10)
    chap = Chapter(number=1, title="C", chapter_summary="", sections=[sec])
    art = Article(
        title="T",
        authors=["A"],
        abstract="",
        target_audience="all",
        chapters=[chap, chap, chap],
    )
    assert check_qg3_outline(art) is True


def test_qg5_readability() -> None:
    """QG-5 should check readability threshold."""
    assert check_qg5_readability(65.0) is True
    assert check_qg5_readability(50.0) is False


def test_qg9_pages() -> None:
    """QG-9 should check minimum page count."""
    assert check_qg9_pages(25) is True
    assert check_qg9_pages(10) is False


def test_run_all_gates() -> None:
    """run_all_gates should aggregate and record results."""
    state = PipelineState(topic="test", run_id="r1")
    results = {
        "bibliography": _make_bibliography(20),
        "hallucination_count": 0,
        "compiled": True,
        "page_count": 30,
    }
    gates = run_all_gates(state, results)
    assert gates["QG-1"] is True
    assert gates["QG-2"] is True
    assert "QG-1" in state.quality_gates_passed
