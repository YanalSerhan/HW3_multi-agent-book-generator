"""Unit tests for crew creation functions and quality gates."""

from unittest.mock import MagicMock, patch

from crewai_book.domain.entities import Article, Chapter, Section
from crewai_book.domain.state import PipelineState
from crewai_book.workflows.quality_gates import (
    check_qg4_word_count,
    check_qg7_citations,
    check_qg8_compilation,
    run_all_gates,
)


@patch("crewai_book.workflows.research_crew.Crew")
@patch("crewai_book.workflows.research_crew.Task")
def test_research_crew_creation(mock_task: MagicMock, mock_crew: MagicMock) -> None:
    """Research crew should be created with 3 agents and 3 tasks."""
    from crewai_book.workflows.research_crew import create_research_crew

    create_research_crew("test topic")
    mock_crew.assert_called_once()
    call_kwargs = mock_crew.call_args
    assert len(call_kwargs.kwargs["agents"]) == 3
    assert len(call_kwargs.kwargs["tasks"]) == 3


@patch("crewai_book.workflows.editorial_crew.Crew")
@patch("crewai_book.workflows.editorial_crew.Task")
def test_editorial_crew_creation(mock_task: MagicMock, mock_crew: MagicMock) -> None:
    """Editorial crew should be created with 2 agents and 2 tasks."""
    from crewai_book.workflows.editorial_crew import create_editorial_crew

    create_editorial_crew()
    mock_crew.assert_called_once()
    call_kwargs = mock_crew.call_args
    assert len(call_kwargs.kwargs["agents"]) == 2
    assert len(call_kwargs.kwargs["tasks"]) == 2


@patch("crewai_book.workflows.main_crew.Crew")
@patch("crewai_book.workflows.main_crew.Task")
def test_main_crew_creation(mock_task: MagicMock, mock_crew: MagicMock) -> None:
    """Main crew should be created with 5 agents and 5 tasks."""
    from crewai_book.workflows.main_crew import create_main_crew

    create_main_crew("test topic")
    mock_crew.assert_called_once()
    call_kwargs = mock_crew.call_args
    assert len(call_kwargs.kwargs["agents"]) == 5
    assert len(call_kwargs.kwargs["tasks"]) == 5


@patch("crewai_book.workflows.main_crew.create_editorial_crew")
@patch("crewai_book.workflows.main_crew.create_main_crew")
@patch("crewai_book.workflows.main_crew.create_research_crew")
def test_run_pipeline(
    mock_research: MagicMock,
    mock_main: MagicMock,
    mock_editorial: MagicMock,
) -> None:
    """run_pipeline should execute all three crews and return state."""
    from crewai_book.workflows.main_crew import run_pipeline

    mock_research.return_value.kickoff.return_value = None
    mock_main.return_value.kickoff.return_value = None
    mock_editorial.return_value.kickoff.return_value = None

    state = run_pipeline("test topic")
    assert state.current_stage == "complete"
    assert state.topic == "test topic"
    mock_research.assert_called_once()
    mock_main.assert_called_once()
    mock_editorial.assert_called_once()


def test_qg4_word_count_pass() -> None:
    """QG-4 should pass when word count is within range."""
    sec = Section(title="S", content="word " * 1500, word_count=1500)
    chap = Chapter(number=1, title="C", chapter_summary="", sections=[sec])
    art = Article(
        title="T",
        authors=["A"],
        abstract="",
        target_audience="all",
        chapters=[chap],
    )
    assert check_qg4_word_count(art, target=1500) is True


def test_qg4_word_count_fail() -> None:
    """QG-4 should fail when word count is too low."""
    sec = Section(title="S", content="word", word_count=1)
    chap = Chapter(number=1, title="C", chapter_summary="", sections=[sec])
    art = Article(
        title="T",
        authors=["A"],
        abstract="",
        target_audience="all",
        chapters=[chap],
    )
    assert check_qg4_word_count(art, target=15000) is False


def test_qg7_citations() -> None:
    """QG-7 should check bib vs ref counts."""
    assert check_qg7_citations(20, 15) is True
    assert check_qg7_citations(5, 15) is False
    assert check_qg7_citations(0, 0) is False


def test_qg8_compilation() -> None:
    """QG-8 should reflect compilation status."""
    assert check_qg8_compilation(True) is True
    assert check_qg8_compilation(False) is False


def test_run_all_gates_with_article() -> None:
    """run_all_gates should include article-based gates."""
    state = PipelineState(topic="test", run_id="r1")
    sec = Section(title="S", content="text " * 1600, word_count=1600)
    chap = Chapter(number=1, title="C", chapter_summary="", sections=[sec])
    art = Article(
        title="T",
        authors=["A"],
        abstract="",
        target_audience="all",
        chapters=[chap, chap, chap],
    )
    results = {
        "article": art,
        "readability_score": 75.0,
    }
    gates = run_all_gates(state, results)
    assert "QG-3" in gates
    assert "QG-5" in gates
    assert gates["QG-5"] is True
