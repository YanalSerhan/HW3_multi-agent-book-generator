"""Unit tests for workflow components."""

from unittest.mock import MagicMock, patch

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.domain.entities import Article, Chapter, Section
from crewai_book.domain.state import Bibliography, Citation, PipelineState
from crewai_book.workflows.gates_runner import run_all_gates
from crewai_book.workflows.quality_gates import (
    check_qg1_sources,
    check_qg2_hallucinations,
    check_qg3_outline,
    check_qg5_readability,
    check_qg9_pages,
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
    state = PipelineState(
        topic="test", run_id="r1", artifacts={"bibliography": _make_bibliography(15)}
    )
    res = check_qg1_sources(state)
    assert res.passed is True


def test_qg1_fail() -> None:
    """QG-1 should fail with <15 sources."""
    state = PipelineState(
        topic="test", run_id="r1", artifacts={"bibliography": _make_bibliography(5)}
    )
    assert check_qg1_sources(state).passed is False


def test_qg2_hallucinations() -> None:
    """QG-2 should pass with 0 hallucinations."""
    state1 = PipelineState(topic="test", run_id="r1", artifacts={"hallucination_count": 0})
    state2 = PipelineState(topic="test", run_id="r1", artifacts={"hallucination_count": 1})
    assert check_qg2_hallucinations(state1).passed is True
    assert check_qg2_hallucinations(state2).passed is False


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
    state = PipelineState(topic="test", run_id="r1", artifacts={"article": art})
    assert check_qg3_outline(state).passed is True


def test_qg5_readability() -> None:
    """QG-5 should check readability threshold."""
    state1 = PipelineState(topic="test", run_id="r1", artifacts={"readability_score": 65.0})
    state2 = PipelineState(topic="test", run_id="r1", artifacts={"readability_score": 50.0})
    assert check_qg5_readability(state1).passed is True
    assert check_qg5_readability(state2).passed is False


def test_qg9_pages() -> None:
    """QG-9 should check minimum page count."""
    state1 = PipelineState(topic="test", run_id="r1", artifacts={"page_count": 25})
    state2 = PipelineState(topic="test", run_id="r1", artifacts={"page_count": 10})
    assert check_qg9_pages(state1).passed is True
    assert check_qg9_pages(state2).passed is False


def test_run_all_gates() -> None:
    """run_all_gates should aggregate and record results."""
    state = PipelineState(
        topic="test",
        run_id="r1",
        artifacts={
            "bibliography": _make_bibliography(20),
            "hallucination_count": 0,
            "compiled": True,
            "page_count": 30,
        },
    )
    gates = run_all_gates(state)
    assert gates["QG-1"] is True
    assert gates["QG-2"] is True
    assert "QG-1" in state.quality_gates_passed
