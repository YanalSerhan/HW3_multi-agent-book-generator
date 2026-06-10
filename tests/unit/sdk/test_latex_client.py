from unittest.mock import MagicMock, patch

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.exceptions.domain import CompilationError
from crewai_book.sdk.latex_client import LaTeXClient


@patch("crewai_book.sdk.latex_client.subprocess.run")
def test_latex_client_success(mock_run, tmp_path) -> None:
    """Test docstring."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Success log"
    mock_run.return_value = mock_result

    test_file = tmp_path / "test.tex"
    test_file.touch()

    client = LaTeXClient()
    result = client.compile_pdf(str(test_file))

    assert result == "Success log"
    assert mock_run.call_count == 6


def test_latex_client_file_not_found() -> None:
    """Test docstring."""
    client = LaTeXClient()
    with pytest.raises(CompilationError, match="Target file not found"):
        client.compile_pdf("/non/existent/file.tex")


@patch("crewai_book.sdk.latex_client.subprocess.run")
def test_latex_client_compilation_error(mock_run, tmp_path) -> None:
    """Test docstring."""
    from crewai_book.exceptions.domain import APIConnectionError
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = "Failure log"
    mock_result.stderr = "Error details"
    mock_run.return_value = mock_result

    test_file = tmp_path / "test.tex"
    test_file.touch()

    client = LaTeXClient()
    with pytest.raises(APIConnectionError, match="Failed after 3 retries"):
        client.compile_pdf(str(test_file))


@patch("crewai_book.sdk.latex_client.subprocess.run")
def test_latex_client_timeout(mock_run, tmp_path) -> None:
    """Test docstring."""
    import subprocess

    from crewai_book.exceptions.domain import APIConnectionError
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="latexmk", timeout=60.0)

    test_file = tmp_path / "test.tex"
    test_file.touch()

    client = LaTeXClient()
    with pytest.raises(APIConnectionError, match="Failed after 3 retries"):
        client.compile_pdf(str(test_file))


@patch("crewai_book.sdk.latex_client.subprocess.run")
def test_latex_client_latexmk_not_found(mock_run, tmp_path) -> None:
    """Test docstring."""
    from crewai_book.exceptions.domain import APIConnectionError
    mock_run.side_effect = FileNotFoundError()

    test_file = tmp_path / "test.tex"
    test_file.touch()

    client = LaTeXClient()
    with pytest.raises(APIConnectionError, match="Failed after 3 retries"):
        client.compile_pdf(str(test_file))
