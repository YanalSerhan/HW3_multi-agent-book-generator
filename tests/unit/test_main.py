import pytest
import typer
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from crewai_book.__main__ import app, version_callback
from crewai_book.version import __version__
from crewai_book.domain.state import PipelineState

runner = CliRunner()

def test_version_callback_true() -> None:
    """Test version callback exits when true."""
    with pytest.raises(typer.Exit):
        version_callback(True)

def test_version_callback_false() -> None:
    """Test version callback does nothing when false."""
    version_callback(False)

def test_app_version() -> None:
    """Test the --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout

def test_app_info() -> None:
    """Test the info command."""
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "CrewAI Book Generator" in result.stdout

@patch("crewai_book.workflows.pipeline.run_pipeline")
def test_app_run_success(mock_run_pipeline: MagicMock) -> None:
    """Test a successful run command."""
    mock_state = PipelineState(topic="Test Topic", run_id="test-run-id")
    mock_run_pipeline.return_value = mock_state
    
    result = runner.invoke(app, ["run", "--topic", "Test Topic"])
    assert result.exit_code == 0
    assert "Pipeline completed" in result.stdout
    assert "test-run-id" in result.stdout

@patch("crewai_book.workflows.pipeline.run_pipeline")
def test_app_run_failure(mock_run_pipeline: MagicMock) -> None:
    """Test run command failure handling."""
    mock_run_pipeline.side_effect = Exception("Test Error")
    
    result = runner.invoke(app, ["run", "--topic", "Test Topic"])
    assert result.exit_code == 1
    assert "Pipeline failed" in result.stdout
    assert "Test Error" in result.stdout
