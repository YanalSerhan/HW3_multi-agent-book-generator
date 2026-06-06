"""Base exception hierarchy for the application."""

from typing import Dict, Any, Optional

class CrewAIBookError(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}

    def __str__(self) -> str:
        base = self.message
        if self.context:
            base += f" | Context: {self.context}"
        return base
