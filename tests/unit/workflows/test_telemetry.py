from pathlib import Path

from crewai_book.domain.state import PipelineState
from crewai_book.workflows.pipeline_utils import _generate_telemetry_appendix


def test_generate_telemetry_appendix_success(tmp_path: Path) -> None:
    """Test generating telemetry appendix with full data."""
    state = PipelineState(topic="Test Topic", run_id="test-123")
    state.retries_used = 2
    state.quality_gates_passed = ["gate1", "gate2"]

    state.artifacts["tokens"] = {"Research": 1000, "Main": 5000}
    state.artifacts["hallucination_count"] = 0
    state.artifacts["latency"] = {"Research": 15.0, "Main": 45.0}

    _generate_telemetry_appendix(state, tmp_path)

    tex_file = tmp_path / "telemetry.tex"
    assert tex_file.exists()

    tex_content = tex_file.read_text(encoding="utf-8")
    assert "\\chapter{Pipeline Run Statistics}" in tex_content
    assert "Total Tokens Used & 6000" in tex_content
    assert "Retries Invoked & 2" in tex_content
    assert "Quality Gates Passed & 2" in tex_content
    assert "Hallucinations Detected & 0" in tex_content

    try:
        import importlib.util
        has_mpl = importlib.util.find_spec("matplotlib") is not None
    except ImportError:
        has_mpl = False

    if has_mpl:
        assert "telemetry_chart.png" in tex_content
        # The chart should have been generated
        chart_file = tmp_path / "figures" / "telemetry_chart.png"
        assert chart_file.exists()
    else:
        assert "Matplotlib not installed" in tex_content


def test_generate_telemetry_appendix_missing_data(tmp_path: Path) -> None:
    """Test generating telemetry degrades gracefully with missing data."""
    state = PipelineState(topic="Test Topic", run_id="test-456")

    _generate_telemetry_appendix(state, tmp_path)

    tex_file = tmp_path / "telemetry.tex"
    assert tex_file.exists()

    tex_content = tex_file.read_text(encoding="utf-8")
    assert "\\chapter{Pipeline Run Statistics}" in tex_content
    assert "Total Tokens Used & N/A" in tex_content
    assert "telemetry_chart.png" not in tex_content
    assert "No latency data available to plot" in tex_content

def test_generate_telemetry_appendix_with_run_notes(tmp_path: Path) -> None:
    """Test generating telemetry appendix with run notes."""
    state = PipelineState(topic="Test Topic", run_id="test-notes")
    _generate_telemetry_appendix(state, tmp_path, run_notes="Custom run note here")
    tex_file = tmp_path / "telemetry.tex"
    tex_content = tex_file.read_text(encoding="utf-8")
    assert "\\section{Run Notes}" in tex_content
    assert "Custom run note here" in tex_content

def test_generate_telemetry_appendix_exception(tmp_path: Path, mocker) -> None:
    """Test generating telemetry appendix exception handling."""
    state = PipelineState(topic="Test", run_id="test-exc")

    # Mock Path.write_text to raise an exception
    mocker.patch("pathlib.Path.mkdir", side_effect=Exception("Test mock error"))

    _generate_telemetry_appendix(state, tmp_path)

    tex_file = tmp_path / "telemetry.tex"
    # Even if mkdir fails, it catches and writes a fallback to telemetry.tex
    # But wait, if write_text fails inside exception block, it will crash.
    # Let's mock write_text inside the try block to fail, but let the except block write_text succeed.

    def fake_mkdir(*args, **kwargs):
        raise RuntimeError("Simulated error")

    mocker.patch("pathlib.Path.mkdir", side_effect=fake_mkdir)

    # Call it again
    _generate_telemetry_appendix(state, tmp_path)

    tex_content = tex_file.read_text(encoding="utf-8")
    assert "Failed to generate metrics." in tex_content

def test_generate_telemetry_matplotlib_success(tmp_path: Path, mocker) -> None:
    """Test hitting the matplotlib rendering code path."""
    from unittest.mock import MagicMock

    state = PipelineState(topic="Test", run_id="test-mpl")
    state.artifacts["latency"] = {"Research": 15.0}

    # Mock matplotlib and plt so it doesn't fail or actually plot
    mock_matplotlib = MagicMock()
    mock_plt = MagicMock()

    mocker.patch.dict("sys.modules", {"matplotlib": mock_matplotlib, "matplotlib.pyplot": mock_plt})

    _generate_telemetry_appendix(state, tmp_path)

    tex_file = tmp_path / "telemetry.tex"
    tex_content = tex_file.read_text(encoding="utf-8")
    assert "telemetry_chart.png" in tex_content
