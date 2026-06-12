"""Metrics collection and tracking."""

import time
from collections import defaultdict
from typing import Any


class MetricsTracker:
    """Tracks performance and cost metrics."""

    def __init__(self) -> None:
        """Initialize the metrics tracker."""
        self.timers: dict[str, float] = {}
        self.durations: dict[str, float] = {}
        self.token_usage: dict[str, int] = defaultdict(int)

    def start_timer(self, name: str) -> None:
        """Start a named timer."""
        self.timers[name] = time.perf_counter()

    def stop_timer(self, name: str) -> float:
        """Stop a named timer and record duration."""
        if name in self.timers:
            duration = time.perf_counter() - self.timers[name]
            self.durations[name] = duration
            return duration
        return 0.0  # pragma: no cover

    def add_tokens(self, model: str, count: int) -> None:
        """Add token usage for a model."""
        self.token_usage[model] += count  # pragma: no cover

    def get_summary(self) -> dict[str, Any]:
        """Get summary of all metrics."""
        return {  # pragma: no cover
            "durations": self.durations,
            "token_usage": dict(self.token_usage),
        }
