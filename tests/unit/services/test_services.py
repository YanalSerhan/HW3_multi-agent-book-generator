from unittest.mock import MagicMock

from crewai_book.domain.entities import Article, Chapter, Section
from crewai_book.domain.state import Bibliography, Citation
from crewai_book.services.citation_service import CitationService
from crewai_book.services.content_service import ContentService
from crewai_book.services.latex_service import LaTeXService
from crewai_book.services.pdf_service import PDFService
from crewai_book.services.research_service import ResearchService


def test_research_service():
    mock_client = MagicMock()
    mock_client.search_web.return_value = [{"title": "Web Source 1", "link": "http://example.com"}]

    service = ResearchService(search_client=mock_client)
    citations = service.search_for_topic("AI", max_results=1)

    assert len(citations) == 1
    assert citations[0].title == "Web Source 1"
    assert citations[0].url == "http://example.com"


def test_citation_service():
    service = CitationService()
    bib = Bibliography()
    cit = Citation(bibtex_key="key1", title="Title", authors=["John Doe"], year=2024, doi="10.123")
    bib.add_citation(cit)

    result = service.generate_bibtex(bib)
    assert "@article{key1," in result
    assert "author={John Doe}" in result
    assert "doi={10.123}" in result


def test_content_service():
    service = ContentService()

    # Empty readability
    assert service.analyze_readability("") == 0.0

    sec = Section(title="1", content="The quick brown fox jumps over the lazy dog.")
    chap = Chapter(number=1, title="C1", chapter_summary="", sections=[sec])
    art = Article(title="Art", authors=["A"], abstract="", target_audience="all", chapters=[chap])

    is_valid = service.validate_article(art)
    assert is_valid is True


def test_latex_service(tmp_path):
    service = LaTeXService(template_dir=tmp_path)

    sec = Section(title="1", content="Text")
    chap = Chapter(number=1, title="C1", chapter_summary="", sections=[sec])
    art = Article(title="Test Book", authors=["A"], abstract="", target_audience="all", chapters=[chap])

    # Test fallback rendering (no template exists)
    output = service.render_article(art)
    assert "Test Book" in output
    assert "\\documentclass" in output


def test_pdf_service(tmp_path):
    mock_client = MagicMock()
    service = PDFService(latex_client=mock_client)

    source_file = tmp_path / "test.tex"
    source_file.touch()

    expected_pdf = service.build_pdf(source_file)
    assert expected_pdf == source_file.with_suffix(".pdf")
    mock_client.compile_pdf.assert_called_once_with(str(source_file))
