"""Integration tests for the complete pipeline execution."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.workflows.pipeline import run_pipeline

pytestmark = pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Requires OPENAI_API_KEY and LaTeX install"
)


def _simulate_research_crew_kickoff(out_path: Path):
    """Simulates the research crew generating its expected files."""
    research_dir = out_path / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    latex_dir = out_path / "latex"
    latex_dir.mkdir(parents=True, exist_ok=True)

    # Generate mock bibliography with 15 sources (to pass QG-1)
    bib_content = ""
    for i in range(15):
        bib_content += (
            f"@article{{source{i},\n  title={{Source {i}}},\n  author={{Author {i}}}\n}}\n\n"
        )
    (latex_dir / "references.bib").write_text(bib_content, encoding="utf-8")

    # Generate mock verification report with NO hallucinations (to pass QG-2)
    (research_dir / "verification_report.md").write_text("All claims verified.", encoding="utf-8")


def _simulate_main_crew_kickoff(out_path: Path):
    """Simulates the main crew generating the manuscript and body.tex."""
    # Generate mock manuscript with 3 chapters, 1 section each, and enough words to pass QG-4
    # Wait, QG-4 requires 7,500 words. We'll generate a dummy file.

    manuscript = "# Chapter 1\n## Section 1\n" + ("word " * 5000) + "\n"
    manuscript += "# Chapter 2\n## Section 1\n" + ("word " * 5000) + "\n"
    manuscript += "# Chapter 3\n## Section 1\n" + ("word " * 5000) + "\n"

    (out_path / "manuscript.md").write_text(manuscript, encoding="utf-8")

    # Generate mock body.tex
    latex_dir = out_path / "latex"
    latex_dir.mkdir(parents=True, exist_ok=True)
    (latex_dir / "body.tex").write_text("This is the LaTeX body.", encoding="utf-8")

    # Simulate pdf_task successfully compiling the PDF
    (latex_dir / "book.pdf").write_text("Mock PDF content", encoding="utf-8")


def _simulate_editorial_crew_kickoff(out_path: Path):
    """Simulates the editorial crew. The readability is evaluated on the manuscript."""
    pass


@patch("builtins.input", return_value="y")
@patch("crewai_book.workflows.pipeline_stages.create_editorial_crew")
@patch("crewai_book.workflows.pipeline_stages.create_main_crew")
@patch("crewai_book.workflows.pipeline_stages.create_research_crew")
@patch("crewai_book.sdk.latex_client.LaTeXClient.compile_pdf")
def test_pipeline_integration_success(
    mock_compile: MagicMock,
    mock_research: MagicMock,
    mock_main: MagicMock,
    mock_editorial: MagicMock,
    mock_input: MagicMock,
    tmp_path: Path,
) -> None:
    """Test that the pipeline correctly integrates all stages, parses files, and passes quality gates."""
    # Setup mocks to simulate file generation during kickoff
    mock_research_crew = MagicMock()
    mock_research_crew.kickoff.side_effect = lambda: _simulate_research_crew_kickoff(tmp_path)
    mock_research.return_value = mock_research_crew

    mock_main_crew = MagicMock()

    def fake_main_kickoff():
        _simulate_main_crew_kickoff(tmp_path)
        if hasattr(mock_main_crew, "tasks"):
            # run callbacks if present
            for task in mock_main_crew.tasks:
                cb = getattr(task, "callback", None)
                if cb:
                    cb("Simulated output")

    mock_main_crew.kickoff.side_effect = fake_main_kickoff
    # Give it mock tasks so callbacks can be attached (latex task is at index 3)
    mock_main_crew.tasks = [MagicMock() for _ in range(6)]
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

    # Verify Jinja template actually rendered the book.tex and body.tex was written
    book_tex = tmp_path / "latex" / "book.tex"
    body_tex = tmp_path / "latex" / "body.tex"
    assert book_tex.exists()
    assert body_tex.exists()
    assert "Simulated output" in body_tex.read_text(encoding="utf-8")

    # Verify crews were called
    mock_research.assert_called_once()
    mock_main.assert_called_once()
    mock_editorial.assert_called_once()


@patch("builtins.input", return_value="y")
@patch("crewai_book.workflows.pipeline_stages.create_research_crew")
def test_pipeline_integration_retry_logic(
    mock_research: MagicMock,
    mock_input: MagicMock,
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
            (research_dir / "verification_report.md").write_text(
                "All claims verified.", encoding="utf-8"
            )
        else:
            # Second run: Passes QG-1 (15 sources)
            bib_content = ""
            for i in range(15):
                bib_content += f"@article{{source{i},\n  title={{Source {i}}},\n  author={{Author {i}}}\n}}\n\n"
            (latex_dir / "references.bib").write_text(bib_content, encoding="utf-8")
            (research_dir / "verification_report.md").write_text(
                "All claims verified.", encoding="utf-8"
            )

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
    with patch("crewai_book.workflows.pipeline_stages.create_main_crew") as mock_main:
        mock_main_crew = MagicMock()
        mock_main_crew.kickoff.side_effect = lambda: (tmp_path / "manuscript.md").write_text(
            "FAIL", encoding="utf-8"
        )
        mock_main.return_value = mock_main_crew

        state = run_pipeline("Retry Topic", output_dir=tmp_path)

        # It should have retried the research crew exactly once, so call_count is 2
        assert call_count["count"] == 2
        # It should have failed at MAIN stage due to invalid manuscript (word count < 7500)
        # So it aborts or exceeds retries at MAIN stage.
        assert state.current_stage == "main"


@patch("crewai_book.workflows.pipeline_stages.create_research_crew")
@patch("crewai_book.workflows.pipeline_stages.create_main_crew")
@patch("builtins.input", side_effect=["y", "n"])
def test_pipeline_human_review_outline_abort(
    mock_input: MagicMock,
    mock_main: MagicMock,
    mock_research: MagicMock,
    tmp_path: Path,
) -> None:
    """Test that the pipeline correctly aborts when HUMAN_REVIEW_OUTLINE is rejected."""
    # Ensure setting is True
    from crewai_book.config.settings import settings

    settings.human_review_outline = True

    mock_research_crew = MagicMock()
    mock_research_crew.kickoff.side_effect = lambda: _simulate_research_crew_kickoff(tmp_path)
    mock_research.return_value = mock_research_crew

    # For main_crew, we want to simulate the outline_task completing.
    # The callback is attached to tasks[0].
    mock_main_crew = MagicMock()

    # We will simulate kickoff by calling the callback if it was attached.
    def fake_kickoff():
        if hasattr(mock_main_crew, "tasks") and mock_main_crew.tasks:
            cb = getattr(mock_main_crew.tasks[0], "callback", None)
            if cb:
                cb("Simulated Outline Content")

    mock_main_crew.kickoff.side_effect = fake_kickoff
    # We need to give it a task list so the pipeline can attach the callback
    mock_task = MagicMock()
    mock_main_crew.tasks = [mock_task]
    mock_main.return_value = mock_main_crew

    with pytest.raises(SystemExit) as exit_exc:
        run_pipeline("Abort Topic", output_dir=tmp_path)

    assert exit_exc.value.code == 0
    assert mock_input.call_count == 2
    mock_input.assert_called_with("Approve outline? [y = continue / n = abort run]: ")
