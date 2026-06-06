"""Readability score tool for CrewAI agents.

Provides text readability analysis using the textstat library,
enabling editorial agents to assess and enforce readability standards.
"""

from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from textstat import flesch_reading_ease


class ReadabilityInput(BaseModel):
    """Input schema for the readability tool."""

    text: str = Field(..., description="The text to analyze for readability.")


class ReadabilityScoreTool(BaseTool):
    """Analyze the readability of a text passage.

    Uses the Flesch Reading Ease score to determine how accessible
    a piece of text is. Scores above 60 indicate the text is
    suitable for the target audience (graduate level).
    """

    name: str = "readability_score"
    description: str = (
        "Calculate the Flesch Reading Ease score for a text. "
        "Scores: 90-100 very easy, 60-70 standard, 30-50 difficult, 0-30 very difficult."
    )
    args_schema: type[BaseModel] = ReadabilityInput

    def _run(self, text: str, **kwargs: Any) -> str:
        """Calculate readability score."""
        if not text.strip():
            return "ERROR: Empty text provided."

        score = float(flesch_reading_ease(text))
        word_count = len(text.split())

        label = self._score_label(score)

        return (
            f"Readability Analysis:\n"
            f"  Flesch Reading Ease: {score:.1f} ({label})\n"
            f"  Word Count: {word_count}\n"
            f"  Target: ≥60.0 (standard difficulty)"
        )

    @staticmethod
    def _score_label(score: float) -> str:
        """Return a human-readable label for the score."""
        if score >= 90:
            return "Very Easy"
        if score >= 70:
            return "Easy"
        if score >= 60:
            return "Standard"
        if score >= 30:
            return "Difficult"
        return "Very Difficult"
