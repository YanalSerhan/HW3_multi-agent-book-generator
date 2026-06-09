"""Base exception hierarchy for the application."""

from enum import Enum
from typing import Any


class PipelineStage(Enum):
    """Stages of the document generation pipeline."""

    INITIALIZATION = "initialization"
    RESEARCH = "research"
    OUTLINE = "outline"
    WRITING = "writing"
    EDITING = "editing"
    REVIEW = "review"
    PRODUCTION = "production"
    QUALITY_ASSURANCE = "quality_assurance"
    UNKNOWN = "unknown"


class CrewAIBookError(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        recoverable: bool = False,
        stage: PipelineStage = PipelineStage.UNKNOWN,
    ) -> None:
        """Initialize."""
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.recoverable = recoverable
        self.stage = stage

    def __str__(self) -> str:
        """Return formatted error message."""
        base = f"[{self.stage.value.upper()}] {self.message}"
        if self.context:
            base += f" | Context: {self.context}"
        base += f" | Recoverable: {self.recoverable}"
        return base
