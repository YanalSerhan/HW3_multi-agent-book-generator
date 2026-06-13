"""Shared test fixtures, mocks, and configuration for the test suite."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import MagicMock

# pyrefly: ignore [missing-import]
import pytest

# Set test environment variables before anything else loads
os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-testing"
os.environ["SERPER_API_KEY"] = "mock-serper-key"
os.environ["TOPIC"] = "Test Topic"
os.environ["OUTPUT_DIR"] = "output"
os.environ["OPENAI_API_URL"] = "https://api.openai.com/v1"
os.environ["SERPER_API_URL"] = "https://google.serper.dev/search"
os.environ["DOI_RESOLVE_URL"] = "https://doi.org"

# We must import these after setting environment variables so pydantic can load properly
from crewai_book.config.settings import AppSettings
from crewai_book.domain.entities import Article, Chapter, Section


@pytest.fixture
def mock_llm() -> MagicMock:
    """Returns a mock LLM that returns deterministic responses."""
    llm = MagicMock()
    llm.invoke.return_value = "Mocked LLM Response"
    return llm


@pytest.fixture
def mock_search_client() -> MagicMock:
    """Returns a mock search client with a pre-seeded source list."""
    client = MagicMock()
    client.search.return_value = [
        {"title": "Test Paper 1", "link": "http://test.com", "snippet": "A test"},
    ]
    return client


@pytest.fixture
def sample_settings() -> AppSettings:
    """Returns a Settings instance with test-safe values."""
    return AppSettings(
        OPENAI_API_KEY="sk-test-key",
        SERPER_API_KEY="test-serper-key",
        OPENAI_API_URL="https://api.openai.com/v1",
        SERPER_API_URL="https://google.serper.dev/search",
        DOI_RESOLVE_URL="https://doi.org",
    )


@pytest.fixture
def sample_research_corpus() -> dict[str, Any]:
    """Returns a realistic but synthetic research corpus."""
    return {
        "topic": "Machine Learning",
        "sources": [
            {
                "title": "Attention Is All You Need",
                "authors": ["Vaswani et al."],
                "year": 2017,
                "url": "https://arxiv.org/abs/1706.03762",
                "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
                "relevance_score": 0.95,
                "credibility_score": 0.99,
            }
        ],
    }


@pytest.fixture
def sample_manuscript() -> Article:
    """Returns a complete synthetic manuscript for editor/formatter tests."""
    section = Section(
        title="Introduction to ML",
        content="Machine learning is fascinating.",
        word_count=5,
        citations=[],
    )
    chapter = Chapter(
        number=1, title="Introduction", sections=[section], chapter_summary="A brief intro."
    )
    return Article(
        title="Test Book",
        authors=["AI Author"],
        abstract="This is a test book.",
        target_audience="General audience",
        chapters=[chapter],
    )


@pytest.fixture
def sample_bib_file(tmp_path) -> str:
    """Creates a temporary .bib file for citation tests."""
    bib_path = tmp_path / "references.bib"
    bib_content = """
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and others},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}
"""
    bib_path.write_text(bib_content)
    return str(bib_path)
