import pytest
from pydantic import ValidationError

from crewai_book.domain.state import Bibliography, Citation, PipelineState


def test_citation_validation() -> None:
    """Test docstring."""
    # Valid citation
    cit = Citation(
        bibtex_key="smith2023", title="AI in Education", authors=["John Smith"], year=2023
    )
    assert cit.year == 2023

    # Invalid year
    with pytest.raises(ValidationError):
        Citation(bibtex_key="future", title="Time Travel", authors=["Doc Brown"], year=3000)


def test_bibliography_deduplication() -> None:
    """Test docstring."""
    bib = Bibliography()
    cit1 = Citation(
        bibtex_key="a1", title="Paper A", authors=["Author"], year=2020, doi="10.1/123"
    )
    cit2 = Citation(
        bibtex_key="a2", title="Paper A", authors=["Author"], year=2020, doi="10.1/123"
    )
    cit3 = Citation(bibtex_key="b1", title="Paper B", authors=["Author"], year=2021)

    bib.add_citation(cit1)
    bib.add_citation(cit2)  # Should not be added (duplicate DOI and title)
    bib.add_citation(cit3)  # Should be added

    assert len(bib.entries) == 2


def test_pipeline_state_tracking() -> None:
    """Test docstring."""
    state = PipelineState(topic="Machine Learning", run_id="run-123")

    state.add_error("research", "Search failed")
    assert len(state.errors) == 1
    assert state.errors[0]["stage"] == "research"

    state.mark_gate_passed("QG-1")
    state.mark_gate_passed("QG-1")  # Deduplication test
    assert len(state.quality_gates_passed) == 1
