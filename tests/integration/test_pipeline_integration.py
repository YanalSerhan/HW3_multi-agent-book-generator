"""Integration tests for the complete pipeline execution."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from crewai_book.workflows.pipeline import run_pipeline


def _simulate_research_crew_kickoff(out_path: Path):
    """Simulates the research crew generating its expected files."""
    research_dir = out_path / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    latex_dir = out_path / "latex"
    latex_dir.mkdir(parents=True, exist_ok=True)

    # Generate mock bibliography with 15 sources (to pass QG-1)
    bib_content = ""
    for i in range(15):
        bib_content += f"@article{{source{i},\n  title={{Source {i}}},\n  author={{Author {i}}}\n}}\n\n"
    (latex_dir / "references.bib").write_text(bib_content, encoding="utf-8")

    # Generate mock verification report with NO hallucinations (to pass QG-2)
    (research_dir / "verification_report.md").write_text("All claims verified.", encoding="utf-8")


def _simulate_main_crew_kickoff(out_path: Path):
    """Simulates the main crew generating the manuscript and body.tex."""
    # Generate mock manuscript with 3 chapters, 1 section each, and enough words to pass QG-4
    # Wait, QG-4 requires 15,000 words. We'll generate a dummy file.
    
    manuscript = "# Chapter 1\n## Section 1\n" + ("word " * 5000) + "\n"
    manuscript += "# Chapter 2\n## Section 1\n" + ("word " * 5000) + "\n"
    manuscript += "# Chapter 3\n## Section 1\n" + ("word " * 5000) + "\n"
    
    (out_path / "manuscript.md").write_text(manuscript, encoding="utf-8")
    
    # Generate mock body.tex
    latex_dir = out_path / "latex"
    latex_dir.mkdir(parents=True, exist_ok=True)
    (latex_dir / "body.tex").write_text("This is the LaTeX body.", encoding="utf-8")


def _simulate_editorial_crew_kickoff(out_path: Path):
    """Simulates the editorial crew. The readability is evaluated on the manuscript."""
    pass


@patch("crewai_book.workflows.pipeline.create_editorial_crew")
@patch("crewai_book.workflows.pipeline.create_main_crew")
@patch("crewai_book.workflows.pipeline.create_research_crew")
@patch("crewai_book.sdk.latex_client.LaTeXClient.compile_pdf")
def test_pipeline_integration_success(
    mock_compile: MagicMock,
    mock_research: MagicMock,
    mock_main: MagicMock,
    mock_editorial: MagicMock,
    tmp_path: Path,
) -> None:
    """Test that the pipeline correctly integrates all stages, parses files, and passes quality gates."""
    
    # Setup mocks to simulate file generation during kickoff
    mock_research_crew = MagicMock()
    mock_research_crew.kickoff.side_effect = lambda: _simulate_research_crew_kickoff(tmp_path)
    mock_research.return_value = mock_research_crew

    mock_main_crew = MagicMock()
    mock_main_crew.kickoff.side_effect = lambda: _simulate_main_crew_kickoff(tmp_path)
    mock_main.return_value = mock_main_crew

    mock_ed_crew = MagicMock()
    mock_ed_crew.kickoff.side_effect = lambda: _simulate_editorial_crew_kickoff(tmp_path)
    mock_editorial.return_value = mock_ed_crew

    # Run the pipeline
    state = run_pipeline("Integration Test Topic", output_dir=tmp_path)

    # Assertions
    assert state.current_stage == "complete"
    assert state.topic == "Integration Test Topic"
    
    # Verify the artifacts were actually parsed and populated in the state
    assert state.artifacts["bib_count"] == 15
    assert state.artifacts["hallucination_count"] == 0
    assert state.artifacts["compiled"] is True
    
    # Verify Jinja template actually rendered the book.tex
    book_tex = (tmp_path / "latex" / "book.tex")
    assert book_tex.exists()
    assert "This is the LaTeX body." in book_tex.read_text(encoding="utf-8")

    # Verify crews were called
    mock_research.assert_called_once()
    mock_main.assert_called_once()
    mock_editorial.assert_called_once()


@patch("crewai_book.workflows.pipeline.create_research_crew")
def test_pipeline_integration_retry_logic(
    mock_research: MagicMock,
    tmp_path: Path,
) -> None:
    """Test that the pipeline correctly triggers a retry if a quality gate fails."""
    
    call_count = {"count": 0}
    
    def _failing_then_passing_research():
        call_count["count"] += 1
        research_dir = tmp_path / "research"
        research_dir.mkdir(parents=True, exist_ok=True)
        latex_dir = tmp_path / "latex"
        latex_dir.mkdir(parents=True, exist_ok=True)

        if call_count["count"] == 1:
            # First run: Fails QG-1 (Only 5 sources)
            bib_content = ""
            for i in range(5):
                bib_content += f"@article{{source{i},\n  title={{Source {i}}},\n  author={{Author {i}}}\n}}\n\n"
            (latex_dir / "references.bib").write_text(bib_content, encoding="utf-8")
            (research_dir / "verification_report.md").write_text("All claims verified.", encoding="utf-8")
        else:
            # Second run: Passes QG-1 (15 sources)
            bib_content = ""
            for i in range(15):
                bib_content += f"@article{{source{i},\n  title={{Source {i}}},\n  author={{Author {i}}}\n}}\n\n"
            (latex_dir / "references.bib").write_text(bib_content, encoding="utf-8")
            (research_dir / "verification_report.md").write_text("All claims verified.", encoding="utf-8")

    mock_research_crew = MagicMock()
    mock_research_crew.kickoff.side_effect = _failing_then_passing_research
    mock_research.return_value = mock_research_crew

    # We patch main_crew and editorial_crew to just abort the pipeline so we don't have to write full mocks
    # We just want to test that the research loop retried successfully.
    with patch("crewai_book.workflows.pipeline._evaluate_gates_for_stage") as mock_eval:
        # Let research pass its gate check (since we are testing the internal gate logic, we actually 
        # want the real _evaluate_gates_for_stage to run for RESEARCH, so we won't mock it for RESEARCH).
        pass

    # Actually, let's just let it fail at MAIN stage to stop the pipeline, so we can verify RESEARCH retried.
    with patch("crewai_book.workflows.pipeline.create_main_crew") as mock_main:
        mock_main_crew = MagicMock()
        mock_main_crew.kickoff.side_effect = lambda: (tmp_path / "manuscript.md").write_text("FAIL", encoding="utf-8")
        mock_main.return_value = mock_main_crew
        
        state = run_pipeline("Retry Topic", output_dir=tmp_path)
        
        # It should have retried the research crew exactly once, so call_count is 2
        assert call_count["count"] == 2
        # It should have failed at MAIN stage due to invalid manuscript (word count < 15000)
        # So it aborts or exceeds retries at MAIN stage.
        assert state.current_stage == "main"
