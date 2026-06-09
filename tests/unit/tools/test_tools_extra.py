"""Additional tool tests to improve coverage on edge cases."""

from unittest.mock import MagicMock, patch

from crewai_book.tools.citation_validator_tool import CitationValidatorTool
from crewai_book.tools.readability_tool import ReadabilityScoreTool


@patch("crewai_book.tools.citation_validator_tool.httpx.Client")
def test_citation_validator_url_valid(mock_client_cls: MagicMock) -> None:
    """CitationValidatorTool should validate reachable URLs."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_client.head.return_value = MagicMock(status_code=200)

    tool = CitationValidatorTool()
    result = tool._run(url="https://example.com")
    assert "VALID" in result


@patch("crewai_book.tools.citation_validator_tool.httpx.Client")
def test_citation_validator_url_invalid(mock_client_cls: MagicMock) -> None:
    """CitationValidatorTool should report unreachable URLs."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.head.return_value = mock_response
    mock_client.get.return_value = mock_response

    tool = CitationValidatorTool()
    result = tool._run(url="https://example.com/missing")
    assert "INVALID" in result


@patch("crewai_book.tools.citation_validator_tool.httpx.Client")
def test_citation_validator_doi_invalid(mock_client_cls: MagicMock) -> None:
    """CitationValidatorTool should report unresolvable DOIs."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.head.return_value = mock_response
    mock_client.get.return_value = mock_response

    tool = CitationValidatorTool()
    result = tool._run(doi="10.9999/fake")
    assert "INVALID" in result


import httpx


@patch("crewai_book.tools.citation_validator_tool.httpx.Client")
def test_citation_validator_doi_network_error(mock_client_cls: MagicMock) -> None:
    """CitationValidatorTool should handle network errors for DOI."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_client.head.side_effect = httpx.ConnectError("timeout")

    tool = CitationValidatorTool()
    result = tool._run(doi="10.1000/test")
    assert "ERROR" in result


@patch("crewai_book.tools.citation_validator_tool.httpx.Client")
def test_citation_validator_url_network_error(mock_client_cls: MagicMock) -> None:
    """CitationValidatorTool should handle network errors for URL."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_client.head.side_effect = httpx.ConnectError("timeout")

    tool = CitationValidatorTool()
    result = tool._run(url="https://example.com")
    assert "ERROR" in result


def test_readability_very_easy() -> None:
    """ReadabilityScoreTool should label very easy text."""
    tool = ReadabilityScoreTool()
    assert tool._score_label(95.0) == "Very Easy"


def test_readability_easy() -> None:
    """ReadabilityScoreTool should label easy text."""
    tool = ReadabilityScoreTool()
    assert tool._score_label(75.0) == "Easy"


def test_readability_standard() -> None:
    """ReadabilityScoreTool should label standard text."""
    tool = ReadabilityScoreTool()
    assert tool._score_label(65.0) == "Standard"


def test_readability_difficult() -> None:
    """ReadabilityScoreTool should label difficult text."""
    tool = ReadabilityScoreTool()
    assert tool._score_label(40.0) == "Difficult"


def test_readability_very_difficult() -> None:
    """ReadabilityScoreTool should label very difficult text."""
    tool = ReadabilityScoreTool()
    assert tool._score_label(20.0) == "Very Difficult"
