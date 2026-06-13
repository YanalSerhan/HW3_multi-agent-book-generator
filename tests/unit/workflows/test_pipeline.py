"""Unit tests for pipeline handoff."""

from pathlib import Path

from crewai_book.domain.state import PipelineState
from crewai_book.workflows.pipeline_utils import _render_latex_callback


class MockOutput:
    def __init__(self, raw: str):
        self.raw = raw


def test_latex_handoff_existence_gate(tmp_path: Path) -> None:
    """Test that render_latex_callback dynamically writes body.tex from output."""
    state = PipelineState(topic="Test Topic", run_id="r1")
    latex_dir = tmp_path / "latex"
    latex_dir.mkdir(parents=True, exist_ok=True)

    # 1. Test successful rendering and dynamic writing
    mock_output = MockOutput("Hello World")
    _render_latex_callback(mock_output, tmp_path, state)

    body_path = latex_dir / "body.tex"
    book_path = latex_dir / "book.tex"

    assert body_path.exists()
    assert "Hello World" in body_path.read_text(encoding="utf-8")
    assert book_path.exists()
    assert "Hello World" in book_path.read_text(encoding="utf-8")
