from textstat import flesch_reading_ease

from ..domain.entities import Article
from ..observability.logger import get_logger


class ContentService:
    """Service to handle content assembly and metrics."""

    def __init__(self) -> None:
        self.logger = get_logger("service.content")

    def analyze_readability(self, text: str) -> float:
        """Calculate the Flesch Reading Ease score."""
        if not text.strip():
            return 0.0
        score = float(flesch_reading_ease(text))
        self.logger.debug(f"Calculated Flesch score: {score}")
        return score

    def validate_article(self, article: Article) -> bool:
        """Validate if the article meets minimum standards."""
        # Calculate full content text
        full_text = []
        for chapter in article.chapters:
            for section in chapter.sections:
                full_text.append(section.content)

        content = " ".join(full_text)
        readability = self.analyze_readability(content)

        self.logger.info(f"Article total words: {article.total_word_count}, Readability: {readability}")

        if readability < 60.0:
            self.logger.warning("Article readability is below 60.0 target.")

        return True
