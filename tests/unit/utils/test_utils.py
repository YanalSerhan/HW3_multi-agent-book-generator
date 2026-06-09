"""Unit tests for utility functions."""

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.exceptions.base import CrewAIBookError
from crewai_book.exceptions.domain import RetryExhaustedError
from crewai_book.utils.retry import retry_recoverable
from crewai_book.utils.sanitize import sanitize_latex


def test_sanitize_latex() -> None:
    """Test LaTeX special character escaping."""
    # Test simple characters
    assert sanitize_latex("test & case") == r"test \& case"
    assert sanitize_latex("100%") == r"100\%"
    assert sanitize_latex("$10") == r"\$10"

    # Test complex/multiple characters
    complex_str = "H_2O & #tags {braces} ~ ^ \\"
    expected = r"H\_2O \& \#tags \{braces\} \textasciitilde{} \textasciicircum{} \textbackslash{}"
    assert sanitize_latex(complex_str) == expected


def test_retry_recoverable_success() -> None:
    """Test retry decorator on success."""
    call_count = 0

    @retry_recoverable(max_attempts=3, initial_backoff=0.01)
    def flappy_function() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise CrewAIBookError("Recoverable error", recoverable=True)
        return "success"

    assert flappy_function() == "success"
    assert call_count == 2


def test_retry_recoverable_exhausted() -> None:
    """Test retry decorator when max attempts are exhausted."""
    call_count = 0

    @retry_recoverable(max_attempts=2, initial_backoff=0.01)
    def failing_function() -> None:
        nonlocal call_count
        call_count += 1
        raise CrewAIBookError("Always fails", recoverable=True)

    with pytest.raises(RetryExhaustedError):
        failing_function()

    assert call_count == 2


def test_retry_unrecoverable() -> None:
    """Test retry decorator raises immediately on unrecoverable errors."""
    call_count = 0

    @retry_recoverable(max_attempts=3, initial_backoff=0.01)
    def fatal_function() -> None:
        nonlocal call_count
        call_count += 1
        raise CrewAIBookError("Fatal error", recoverable=False)

    with pytest.raises(CrewAIBookError) as exc_info:
        fatal_function()

    assert exc_info.value.recoverable is False
    assert call_count == 1
