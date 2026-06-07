from unittest.mock import MagicMock, patch

from crewai_book.sdk.search_client import SearchClient


@patch("crewai_book.sdk.search_client.httpx.Client")
def test_search_client_success(mock_client_cls) -> None:
    """Test docstring."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"organic": [{"title": "Result"}]}
    mock_client.post.return_value = mock_resp

    with patch("crewai_book.shared.gatekeeper.time.sleep"):
        client = SearchClient()
        # Mock settings to have an API key
        with patch("crewai_book.sdk.search_client.settings.serper_api_key", "test_key"):
            client.headers["X-API-KEY"] = "test_key"
            res = client.search_web("query")
            assert len(res) == 1
            assert res[0]["title"] == "Result"


def test_search_client_no_api_key() -> None:
    """Test docstring."""
    client = SearchClient()
    with patch("crewai_book.sdk.search_client.settings.serper_api_key", ""):
        res = client.search_web("query")
        assert res == []  # Warning logged and empty list returned
