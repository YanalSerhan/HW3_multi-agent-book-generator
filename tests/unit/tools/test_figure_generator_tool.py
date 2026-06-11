from unittest.mock import MagicMock, patch

from crewai_book.tools.figure_generator_tool import FigureGeneratorTool


def test_figure_generator_invalid_filename() -> None:
    tool = FigureGeneratorTool()
    res = tool._run("print('hello')", "test.txt")
    assert "FAILED: Filename must end with .png or .pdf" in res


def test_figure_generator_invalid_syntax() -> None:
    tool = FigureGeneratorTool()
    res = tool._run("print('hello'", "test.png")
    assert "FAILED: Invalid Python syntax" in res


def test_figure_generator_import_allowlist_rejected() -> None:
    tool = FigureGeneratorTool()
    res1 = tool._run("import os\nos.system('ls')", "test.png")
    assert "FAILED: Security error. Importing 'os' is not allowed" in res1

    res2 = tool._run("from subprocess import run", "test.png")
    assert "FAILED: Security error. Importing from 'subprocess' is not allowed" in res2


def test_figure_generator_dangerous_functions_rejected() -> None:
    tool = FigureGeneratorTool()
    res1 = tool._run("eval('1+1')", "test.png")
    assert "FAILED: Security error. Calling 'eval' is not allowed" in res1

    res2 = tool._run("exec('import os')", "test.png")
    assert "FAILED: Security error. Calling 'exec' is not allowed" in res2


def test_figure_generator_imports_at_top_enforced() -> None:
    tool = FigureGeneratorTool()
    code = "print('hello')\nimport math\n"
    res = tool._run(code, "test.png")
    assert "FAILED: Security error. All imports must be at the top of the module." in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_success(mock_run, tmp_path) -> None:
    def side_effect(*args, **kwargs):
        cwd = kwargs.get("cwd")
        if cwd:
            (cwd / "test.png").touch()
        mock_result = MagicMock()
        mock_result.returncode = 0
        return mock_result

    mock_run.side_effect = side_effect

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("import matplotlib.pyplot as plt\nprint('hello')", "test.png")
        assert "SUCCESS: Figure generated" in res
        mock_run.assert_called_once()
        # Verify it was moved to final destination
        assert (tmp_path / "latex" / "figures" / "test.png").exists()


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_file_not_created(mock_run, tmp_path) -> None:
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("import numpy\nprint('hello')", "test.png")
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
        res = tool._run("import math\nprint('hello')", "test.png")
        assert "FAILED: Code execution error" in res
        assert "some error" in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_timeout(mock_run, tmp_path) -> None:
    import subprocess

    mock_run.side_effect = subprocess.TimeoutExpired(cmd="python", timeout=60.0)

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("import random\nprint('hello')", "test.png")
        assert "FAILED: Code execution timed out" in res


@patch("crewai_book.tools.figure_generator_tool.subprocess.run")
def test_figure_generator_unexpected_error(mock_run, tmp_path) -> None:
    mock_run.side_effect = RuntimeError("Something bad happened")

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        res = tool._run("import seaborn\nprint('hello')", "test.png")
        assert "FAILED: Unexpected error: Something bad happened" in res


def test_figure_generator_path_traversal() -> None:
    tool = FigureGeneratorTool()
    # Test path traversal in the filename itself
    res = tool._run("import random", "../../../etc/passwd.png")
    assert "FAILED: Invalid filename. Must be a simple basename" in res


def test_figure_generator_non_mocked_matplotlib(tmp_path) -> None:
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        import pytest

        pytest.skip("matplotlib not installed")

    with patch("crewai_book.tools.figure_generator_tool.OUTPUT_DIR", tmp_path):
        tool = FigureGeneratorTool()
        code = (
            "import matplotlib.pyplot as plt\n"
            "plt.figure()\n"
            "plt.plot([1, 2, 3])\n"
            "plt.savefig('test_plot.png')\n"
        )
        res = tool._run(code, "test_plot.png")
        assert "SUCCESS: Figure generated" in res
        assert (tmp_path / "latex" / "figures" / "test_plot.png").exists()
