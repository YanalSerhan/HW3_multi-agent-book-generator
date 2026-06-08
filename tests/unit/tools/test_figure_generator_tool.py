from unittest.mock import MagicMock, patch
# pyrefly: ignore [missing-import]
import pytest

from crewai_book.tools.figure_generator_tool import FigureGeneratorTool


def test_figure_generator_invalid_filename() -> None:
    tool = FigureGeneratorTool()
    res = tool._run("print('hello')", "test.txt")
    assert "FAILED: Filename must end with .png or .pdf" in res


def test_figure_generator_invalid_syntax() -> None:
    tool = FigureGeneratorTool()
    res = tool._run("print('hello'", "test.png")
    assert "FAILED: Invalid Python syntax" in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_success(mock_run, tmp_path) -> None:
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        # We need to simulate the file being created
        figures_dir = tmp_path / "latex" / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        target = figures_dir / "test.png"
        target.touch()

        tool = FigureGeneratorTool()
        res = tool._run("print('hello')", "test.png")
        assert "SUCCESS: Figure generated" in res
        mock_run.assert_called_once()


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_file_not_created(mock_run, tmp_path) -> None:
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("print('hello')", "test.png")
        assert "FAILED: The code executed successfully but the file" in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_execution_error(mock_run, tmp_path) -> None:
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = "some output"
    mock_result.stderr = "some error"
    mock_run.return_value = mock_result

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("print('hello')", "test.png")
        assert "FAILED: Code execution error" in res
        assert "some error" in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_timeout(mock_run, tmp_path) -> None:
    import subprocess
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="python", timeout=30.0)

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("print('hello')", "test.png")
        assert "FAILED: Code execution timed out" in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_unexpected_error(mock_run, tmp_path) -> None:
    mock_run.side_effect = RuntimeError("Something bad happened")

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("print('hello')", "test.png")
        assert "FAILED: Unexpected error: Something bad happened" in res
