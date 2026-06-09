import queue
import threading
import time
from collections.abc import Callable
from typing import Any

from ..config.settings import config_manager
from ..exceptions.domain import RateLimitExceededError


class ApiGatekeeper:
    """Centralized gatekeeper for all external API calls.

    Enforces rate limits and provides queued execution with retries.
    """

    def __init__(self, service_name: str, max_queue_size: int = 100) -> None:
        """Initialize the gatekeeper for a specific service."""
        self.service_name = service_name
        self._load_config()
        self.request_queue: queue.Queue[int] = queue.Queue(maxsize=max_queue_size)
        self.call_timestamps: list[float] = []
        self._lock = threading.Lock()

    def _load_config(self) -> None:
        """Load rate limits from configuration."""
        limits_cfg = config_manager.get_rate_limits()
        service_limits = limits_cfg.get("limits", {}).get(self.service_name, {})

        self.rpm = service_limits.get("requests_per_minute", 60)
        self.retry_after = service_limits.get("retry_after_seconds", 5)
        self.max_retries = service_limits.get("max_retries", 3)
        self.concurrent_max = service_limits.get("concurrent_max", 5)

    def _enforce_rate_limit(self) -> None:
        """Check and wait if rate limits are exceeded."""
        with self._lock:
            now = time.time()
            # Remove timestamps older than 60 seconds
            self.call_timestamps = [t for t in self.call_timestamps if now - t < 60.0]

            if len(self.call_timestamps) >= self.rpm:
                sleep_time = 60.0 - (now - self.call_timestamps[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)

            self.call_timestamps.append(time.time())

    def execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute a function through the gatekeeper."""
        try:
            self.request_queue.put_nowait(1)
        except queue.Full:
            raise RateLimitExceededError(
                f"Queue full for service {self.service_name}",
                {"max_queue_size": self.request_queue.maxsize},
            ) from None

        try:
            return self._execute_with_retry(func, *args, **kwargs)
        finally:
            self.request_queue.get_nowait()
            self.request_queue.task_done()

    def _execute_with_retry(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute with retry logic for transient failures."""
        from ..exceptions.domain import APIConnectionError
        attempts = 0
        while attempts <= self.max_retries:
            self._enforce_rate_limit()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts > self.max_retries:
                    raise APIConnectionError(
                        f"Failed after {self.max_retries} retries calling {self.service_name}",
                        {"error": str(e)},
                    ) from e
                time.sleep(self.retry_after)

    def get_queue_status(self) -> dict[str, int]:
        """Return the current queue status."""
        return {"current_size": self.request_queue.qsize(), "max_size": self.request_queue.maxsize}
