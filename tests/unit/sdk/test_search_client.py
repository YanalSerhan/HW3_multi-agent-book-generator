from unittest.mock import MagicMock, patch

# pyrefly: ignore [missing-import]
import pytest
from pydantic import SecretStr

from crewai_book.sdk.search_client import SearchClient


@patch("crewai_book.sdk.search_client.httpx.Client")
def test_search_client_success(mock_client_cls: MagicMock) -> None:
    """Test successful search execution."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"organic": [{"title": "Result"}]}
    mock_client.post.return_value = mock_resp

    with patch("crewai_book.shared.gatekeeper.time.sleep"):
        client = SearchClient()
        # Mock settings to have an API key
        with patch("crewai_book.sdk.search_client.settings.serper_api_key", SecretStr("test_key")):
            client.headers["X-API-KEY"] = "test_key"
            res = client.search_web("query")
            assert len(res) == 1
            assert res[0]["title"] == "Result"


def test_search_client_no_api_key() -> None:
    """Test docstring."""
    client = SearchClient()
    with patch("crewai_book.sdk.search_client.settings.serper_api_key", SecretStr("")):
        res = client.search_web("query")
        assert res == []  # Warning logged and empty list returned


@patch("crewai_book.sdk.search_client.httpx.Client")
def test_search_client_httperror(mock_client_cls) -> None:
    """Test HTTPError exception handling."""
    import httpx

    from crewai_book.exceptions.domain import APIConnectionError

    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_client.post.side_effect = httpx.HTTPError("Request failed")

    client = SearchClient()
    with (
        patch("crewai_book.sdk.search_client.settings.serper_api_key", SecretStr("test_key")),
        pytest.raises(APIConnectionError, match="Search failed"),
    ):
        client.search_web("query")


@patch("crewai_book.sdk.search_client.httpx.Client")
def test_search_client_invalid_data(mock_client_cls) -> None:
    """Test handling of non-dict or non-list responses."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = []  # Not a dict
    mock_client.post.return_value = mock_resp

    client = SearchClient()
    with patch("crewai_book.sdk.search_client.settings.serper_api_key", SecretStr("test_key")):
        res = client.search_web("query")
        assert res == []

    mock_resp.json.return_value = {"organic": "not a list"}
    with patch("crewai_book.sdk.search_client.settings.serper_api_key", SecretStr("test_key")):
        res = client.search_web("query")
        assert res == []


def test_search_arxiv() -> None:
    """Test arxiv search method."""
    client = SearchClient()
    res = client.search_arxiv("query")
    assert res == []
