from unittest.mock import MagicMock, patch

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.exceptions.domain import APIConnectionError
from crewai_book.sdk.llm_client import LLMClient


@patch("crewai_book.sdk.llm_client.httpx.Client")
def test_llm_client_complete_success(mock_client_cls) -> None:
    """Test docstring."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"choices": [{"message": {"content": "Hello World"}}]}
    mock_client.post.return_value = mock_resp

    # We will patch the Gatekeeper delay for speed
    with patch("crewai_book.shared.gatekeeper.time.sleep"):
        client = LLMClient()
        result = client.complete([{"role": "user", "content": "Hi"}])
        assert result == "Hello World"


@patch("crewai_book.sdk.llm_client.httpx.Client")
def test_llm_client_malformed_response(mock_client_cls) -> None:
    """Test docstring."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"invalid": "schema"}
    mock_client.post.return_value = mock_resp

    with patch("crewai_book.shared.gatekeeper.time.sleep"):
        client = LLMClient()
        with pytest.raises(APIConnectionError, match="Malformed"):
            client.complete([])
