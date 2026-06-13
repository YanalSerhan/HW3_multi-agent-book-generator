# pyrefly: ignore [missing-import]
from pathlib import Path
from unittest.mock import MagicMock, patch

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.domain.state import PipelineState
from crewai_book.workflows.gate_models import PipelineStage
from crewai_book.workflows.pipeline_utils import _evaluate_gates_for_stage, _render_latex_callback


def test_evaluate_gates_for_stage_success() -> None:
    state = PipelineState(topic="test", run_id="r1")
    with (
        patch("crewai_book.workflows.pipeline_utils.run_all_gates", return_value={"gate1": True}),
        patch("crewai_book.workflows.pipeline_utils.QUALITY_GATES", []),
    ):
            res = _evaluate_gates_for_stage(state, PipelineStage.RESEARCH)
            assert res is True

def test_evaluate_gates_for_stage_abort() -> None:
    state = PipelineState(topic="test", run_id="r1")
    gate_mock = MagicMock(stage=PipelineStage.RESEARCH, severity="blocking", on_failure="abort")
    gate_mock.name = "gate1"

    with (
        patch("crewai_book.workflows.pipeline_utils.run_all_gates", return_value={"gate1": False}),
        patch("crewai_book.workflows.pipeline_utils.QUALITY_GATES", [gate_mock]),
    ):
            res = _evaluate_gates_for_stage(state, PipelineStage.RESEARCH)
            assert res is False

def test_evaluate_gates_for_stage_retry() -> None:
    state = PipelineState(topic="test", run_id="r1")
    state.retries_used = 0
    gate_mock = MagicMock(stage=PipelineStage.RESEARCH, severity="blocking", on_failure="retry")
    gate_mock.name = "gate1"

    with (
        patch("crewai_book.workflows.pipeline_utils.run_all_gates", return_value={"gate1": False}),
        patch("crewai_book.workflows.pipeline_utils.QUALITY_GATES", [gate_mock]),
    ):
            res = _evaluate_gates_for_stage(state, PipelineStage.RESEARCH)
            assert res == "retry"
            assert state.retries_used == 1

def test_evaluate_gates_for_stage_max_retries() -> None:
    state = PipelineState(topic="test", run_id="r1")
    state.retries_used = 2 # MAX_RETRIES is 2, so it will become 3 > 2
    gate_mock = MagicMock(stage=PipelineStage.RESEARCH, severity="blocking", on_failure="retry")
    gate_mock.name = "gate1"

    with (
        patch("crewai_book.workflows.pipeline_utils.run_all_gates", return_value={"gate1": False}),
        patch("crewai_book.workflows.pipeline_utils.QUALITY_GATES", [gate_mock]),
    ):
            res = _evaluate_gates_for_stage(state, PipelineStage.RESEARCH)
            assert res is False
            assert state.retries_used == 3

@patch("crewai_book.latex.renderer.create_jinja_env")
@patch("crewai_book.latex.renderer.inject_provenance_footnotes")
def test_render_latex_callback(mock_inject, mock_env, tmp_path: Path) -> None:
    out_path = tmp_path / "out"
    latex_dir = out_path / "latex"
    latex_dir.mkdir(parents=True)

    state = PipelineState(topic="test", run_id="r1")

    mock_template = MagicMock()
    mock_template.render.return_value = "Rendered TeX"
    mock_env.return_value.get_template.return_value = mock_template
    mock_inject.return_value = "Injected Content"

    bib_file = latex_dir / "references.bib"
    bib_file.write_text("Dummy", encoding="utf-8")

    # Write a dummy notebook to trigger extraction logic
    src_dir = Path("sources")
    src_dir.mkdir(exist_ok=True)
    hw_nb = src_dir / "vae_homework.ipynb"
    hw_nb.write_text("dummy", encoding="utf-8")

    output = MagicMock(raw="Body Content")

    with (
        patch("crewai_book.latex.post_processor.post_process_latex", return_value="Final TeX"),
        patch("crewai_book.tools.nb_latex_extractor.extract_notebook_to_latex"),
    ):
            _render_latex_callback(output, out_path, state)

    body_file = latex_dir / "body.tex"
    book_file = latex_dir / "book.tex"

    assert body_file.exists()
    assert body_file.read_text(encoding="utf-8") == "Body Content"

    assert book_file.exists()
    assert book_file.read_text(encoding="utf-8") == "Final TeX"

def test_render_latex_callback_exception(tmp_path: Path) -> None:
    out_path = tmp_path / "out"
    latex_dir = out_path / "latex"
    latex_dir.mkdir(parents=True)
    state = PipelineState(topic="test", run_id="r1")

    output = MagicMock(raw="Body Content")

    with (
        patch("crewai_book.latex.post_processor.post_process_latex", side_effect=Exception("Mock Error")),
        pytest.raises(RuntimeError, match="Hard stop: LaTeX render callback failed: Mock Error"),
    ):
            _render_latex_callback(output, out_path, state)
