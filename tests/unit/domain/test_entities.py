from crewai_book.domain.entities import Article, Chapter, Section


def test_section_word_count() -> None:
    """Test docstring."""
    section = Section(
        title="Intro", content="This is a short introduction paragraph with some words."
    )
    section.update_word_count()
    assert section.word_count == 9


def test_chapter_total_word_count() -> None:
    """Test docstring."""
    sec1 = Section(title="1", content="One two three", word_count=3)
    sec2 = Section(title="2", content="Four five", word_count=2)

    chapter = Chapter(
        number=1, title="Chapter 1", chapter_summary="Summary", sections=[sec1, sec2]
    )
    assert chapter.total_word_count == 5


def test_article_total_word_count() -> None:
    """Test docstring."""
    sec1 = Section(title="1", content="", word_count=100)
    chap1 = Chapter(number=1, title="C1", chapter_summary="", sections=[sec1])

    sec2 = Section(title="2", content="", word_count=250)
    chap2 = Chapter(number=2, title="C2", chapter_summary="", sections=[sec2])

    article = Article(
        title="Full Book",
        authors=["Alice"],
        abstract="Abstract",
        target_audience="General",
        chapters=[chap1, chap2],
    )
    assert article.total_word_count == 350
