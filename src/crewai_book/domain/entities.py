from pydantic import BaseModel, Field


class CitationRef(BaseModel):
    """Reference to a citation within the text."""

    bibtex_key: str = Field(..., description="The BibTeX key referring to the citation")


class Section(BaseModel):
    """A specific section within a chapter."""

    title: str = Field(..., description="Title of the section")
    content: str = Field(..., description="Markdown content of the section")
    word_count: int = Field(default=0, ge=0, description="Word count of the content")
    citations: list[CitationRef] = Field(
        default_factory=list, description="Citations used in this section"
    )

    def update_word_count(self) -> None:
        """Update the word count based on current content."""
        self.word_count = len(self.content.split())


class Chapter(BaseModel):
    """A complete chapter consisting of multiple sections."""

    number: int = Field(..., description="Chapter sequence number")
    title: str = Field(..., description="Title of the chapter")
    sections: list[Section] = Field(
        default_factory=list, description="Sections within the chapter"
    )
    chapter_summary: str = Field(..., description="Summary of the chapter content")

    @property
    def total_word_count(self) -> int:
        """Calculate total word count for the chapter."""
        return sum(section.word_count for section in self.sections)


class Article(BaseModel):
    """The root entity representing the complete document."""

    title: str = Field(..., description="Document title")
    authors: list[str] = Field(..., description="List of document authors")
    abstract: str = Field(..., description="Abstract summarizing the entire document")
    chapters: list[Chapter] = Field(default_factory=list, description="Ordered list of chapters")
    target_audience: str = Field(..., description="Intended audience for the document")

    @property
    def total_word_count(self) -> int:
        """Calculate total word count for the entire article."""
        return sum(chapter.total_word_count for chapter in self.chapters)
