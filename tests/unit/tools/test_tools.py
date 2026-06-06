"""Unit tests for CrewAI tool classes."""

from unittest.mock import MagicMock, patch

from crewai_book.tools.arxiv_tool import ArXivTool
from crewai_book.tools.citation_validator_tool import CitationValidatorTool
from crewai_book.tools.fact_check_tool import FactCheckTool
from crewai_book.tools.latex_compiler_tool import LaTeXCompilerTool
from crewai_book.tools.readability_tool import ReadabilityScoreTool
from crewai_book.tools.web_search_tool import WebSearchTool


@patch("crewai_book.tools.web_search_tool.SearchClient")
def test_web_search_tool_returns_formatted_results(mock_cls: MagicMock) -> None:
    """WebSearchTool should format search results into readable text."""
    mock_cls.return_value.search_web.return_value = [
        {"title": "Result 1", "link": "http://example.com", "snippet": "A snippet."},
    ]
    tool = WebSearchTool()
    result = tool._run(query="test query")
    assert "Result 1" in result
    assert "http://example.com" in result


@patch("crewai_book.tools.web_search_tool.SearchClient")
def test_web_search_tool_no_results(mock_cls: MagicMock) -> None:
    """WebSearchTool should handle empty results gracefully."""
    mock_cls.return_value.search_web.return_value = []
    tool = WebSearchTool()
    result = tool._run(query="obscure query")
    assert "No results found" in result


@patch("crewai_book.tools.arxiv_tool.arxiv.Client")
def test_arxiv_tool_returns_papers(mock_client_cls: MagicMock) -> None:
    """ArXivTool should format ArXiv paper metadata."""
    author1 = MagicMock()
    author1.name = "Alice"
    author2 = MagicMock()
    author2.name = "Bob"

    mock_paper = MagicMock()
    mock_paper.title = "Multi-Agent Systems"
    mock_paper.authors = [author1, author2]
    mock_paper.published.strftime.return_value = "2024-01-15"
    mock_paper.entry_id = "http://arxiv.org/abs/1234"
    mock_paper.summary = "A paper about multi-agent systems." * 10

    mock_client_cls.return_value.results.return_value = [mock_paper]

    tool = ArXivTool()
    result = tool._run(query="multi-agent systems", max_results=1)
    assert "Multi-Agent Systems" in result


@patch("crewai_book.tools.citation_validator_tool.httpx.Client")
def test_citation_validator_doi_valid(mock_client_cls: MagicMock) -> None:
    """CitationValidatorTool should confirm valid DOIs."""
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client
    mock_client.head.return_value = MagicMock(status_code=200)

    tool = CitationValidatorTool()
    result = tool._run(doi="10.1000/test")
    assert "VALID" in result


def test_citation_validator_no_input() -> None:
    """CitationValidatorTool should error when no input is given."""
    tool = CitationValidatorTool()
    result = tool._run()
    assert "ERROR" in result


def test_latex_compiler_tool_failure() -> None:
    """LaTeXCompilerTool should report compilation errors."""
    tool = LaTeXCompilerTool()
    result = tool._run(tex_file_path="/nonexistent/file.tex")
    assert "FAILED" in result


def test_readability_tool_valid_text() -> None:
    """ReadabilityScoreTool should return a readability analysis."""
    tool = ReadabilityScoreTool()
    text = "The quick brown fox jumps over the lazy dog. " * 10
    result = tool._run(text=text)
    assert "Flesch Reading Ease" in result
    assert "Word Count" in result


def test_readability_tool_empty_text() -> None:
    """ReadabilityScoreTool should handle empty input."""
    tool = ReadabilityScoreTool()
    result = tool._run(text="   ")
    assert "ERROR" in result


@patch("crewai_book.tools.fact_check_tool.SearchClient")
def test_fact_check_tool_corroborated(mock_cls: MagicMock) -> None:
    """FactCheckTool should report corroboration when sources match."""
    mock_cls.return_value.search_web.return_value = [
        {"title": "AI multi-agent systems confirmed", "snippet": "multi agent systems are real"},
        {"title": "AI agents work", "snippet": "multi agent systems confirmed"},
        {"title": "Agent research", "snippet": "multi agent collaboration"},
    ]
    tool = FactCheckTool()
    result = tool._run(claim="multi agent systems are real")
    assert "Confidence" in result


@patch("crewai_book.tools.fact_check_tool.SearchClient")
def test_fact_check_tool_unverified(mock_cls: MagicMock) -> None:
    """FactCheckTool should report low confidence when no sources found."""
    mock_cls.return_value.search_web.return_value = []
    tool = FactCheckTool()
    result = tool._run(claim="unicorns fly to mars daily")
    assert "UNVERIFIED" in result
