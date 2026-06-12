"""Retry utilities for recoverable errors."""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from loguru import logger

from ..exceptions.base import CrewAIBookError
from ..exceptions.domain import RetryExhaustedError

T = TypeVar("T", bound=Callable[..., Any])


def retry_recoverable(max_attempts: int = 3, initial_backoff: float = 1.0) -> Callable[[T], T]:
    """Retry a function if it raises a recoverable CrewAIBookError.

    Uses exponential backoff for the delay.
    If attempts are exhausted, raises RetryExhaustedError.
    """

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            delay = initial_backoff

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except CrewAIBookError as e:
                    if not e.recoverable:
                        raise e

                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(
                            f"Retry exhausted for {func.__name__} after {max_attempts} attempts. "
                            f"Last error: {e}"
                        )
                        raise RetryExhaustedError(
                            f"Failed after {max_attempts} attempts", context={"last_error": str(e)}
                        ) from e

                    logger.warning(
                        f"Recoverable error in {func.__name__}: {e}. "
                        f"Retrying {attempts}/{max_attempts} in {delay}s..."
                    )
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff

            return None  # pragma: no cover

        return cast(T, wrapper)

    return decorator
