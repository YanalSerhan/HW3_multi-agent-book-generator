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
    assert "telemetry_chart.png" in tex_content

    # The chart should have been generated
    chart_file = tmp_path / "figures" / "telemetry_chart.png"
    assert chart_file.exists()


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
