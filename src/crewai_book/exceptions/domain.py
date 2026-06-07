"""Domain-specific exceptions."""

from .base import CrewAIBookError


class ConfigError(CrewAIBookError):
    """Raised when there is an issue with application configuration."""

    pass


class RateLimitExceededError(CrewAIBookError):
    """Raised when API rate limits are exceeded and back-pressure fails."""

    pass


class APIConnectionError(CrewAIBookError):
    """Raised when an external API cannot be reached."""

    pass


class AgentFailureError(CrewAIBookError):
    """Raised when a CrewAI agent fails to complete its task."""

    pass


class SearchError(CrewAIBookError):
    """Raised when a search query fails."""

    pass


class HallucinationDetectedError(CrewAIBookError):
    """Raised when a critical hallucination is detected by the quality gate."""

    pass


class CompilationError(CrewAIBookError):
    """Raised when LaTeX compilation fails."""

    pass
