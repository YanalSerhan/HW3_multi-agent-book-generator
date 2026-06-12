"""Agent activity tracking."""

from typing import Any


class AgentTracker:
    """Tracks inputs and outputs of agents for observability."""

    def __init__(self) -> None:
        """Initialize the agent tracker."""
        self.activities: list[dict[str, Any]] = []

    def record_activity(
        self, agent_name: str, activity_type: str, details: dict[str, Any]
    ) -> None:
        """Record an activity performed by an agent."""
        self.activities.append(
            {
                "agent": agent_name,
                "type": activity_type,
                "details": details,
            }
        )

    def get_activities(self) -> list[dict[str, Any]]:
        """Retrieve all recorded activities."""
        return self.activities  # pragma: no cover
