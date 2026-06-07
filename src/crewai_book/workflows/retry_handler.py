"""Retry handler for workflow execution.

Provides exponential backoff retry logic for agent tasks and
quality gate re-checks, with configurable max attempts.
"""

import time
from collections.abc import Callable
from typing import Any, TypeVar

from ..observability.logger import get_logger

T = TypeVar("T")

logger = get_logger("workflows.retry")


def retry_with_backoff(
    func: Callable[..., Any],
    max_retries: int = 3,
    base_delay: float = 2.0,
    description: str = "operation",
) -> Any:
    """Execute a function with exponential backoff retry.

    Args:
        func: The callable to execute.
        max_retries: Maximum number of retry attempts.
        base_delay: Base delay in seconds (doubles each retry).
        description: Human-readable description for logging.

    Returns:
        The return value of func on success.

    Raises:
        The last exception if all retries are exhausted.
    """
    last_exception: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            result = func()
            if attempt > 0:
                logger.info(f"{description} succeeded on attempt {attempt + 1}")
            return result
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                delay = base_delay * (2**attempt)
                logger.warning(
                    f"{description} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                time.sleep(delay)
            else:
                logger.error(f"{description} failed after {max_retries + 1} attempts: {e}")

    raise last_exception  # type: ignore[misc]
