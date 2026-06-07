from unittest.mock import MagicMock, patch

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
    mock_run.assert_called_once()


def test_latex_client_file_not_found() -> None:
    """Test docstring."""
    client = LaTeXClient()
    with pytest.raises(CompilationError, match="Target file not found"):
        client.compile_pdf("/non/existent/file.tex")
