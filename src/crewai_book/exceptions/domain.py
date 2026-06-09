"""Domain-specific exceptions."""

from .base import CrewAIBookError


class ConfigurationError(CrewAIBookError):
    """Raised when there is an issue with application configuration."""
    pass


class ResearchError(CrewAIBookError):
    """Base exception for research phase errors."""
    pass


class SearchError(ResearchError):
    """Raised when a search query fails."""
    pass


class CitationValidationError(ResearchError):
    """Raised when a citation is invalid or unresolved."""
    pass


class ContentError(CrewAIBookError):
    """Base exception for content generation and editing errors."""
    pass


class HallucinationDetectedError(ContentError):
    """Raised when a critical hallucination is detected by the quality gate."""
    pass


class QualityGateError(ContentError):
    """Raised when a manuscript fails a quality gate."""
    pass


class LaTeXError(CrewAIBookError):
    """Base exception for LaTeX formatting and compilation errors."""
    pass


class CompilationError(LaTeXError):
    """Raised when LaTeX compilation fails."""
    pass


class TemplateRenderError(LaTeXError):
    """Raised when rendering a LaTeX template fails."""
    pass


class PipelineError(CrewAIBookError):
    """Base exception for general pipeline orchestration errors."""
    pass


class AgentFailureError(PipelineError):
    """Raised when a CrewAI agent fails to complete its task."""
    pass


class RetryExhaustedError(PipelineError):
    """Raised when the maximum number of retries is exhausted."""
    pass


class RateLimitExceededError(CrewAIBookError):
    """Raised when API rate limits are exceeded and back-pressure fails."""
    pass


class APIConnectionError(CrewAIBookError):
    """Raised when an external API cannot be reached."""
    pass
