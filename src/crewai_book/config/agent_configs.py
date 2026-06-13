"""Agent configuration models and constants.

Contains the full role, goal, and backstory definitions for all 11
agents in the multi-agent book generation pipeline, as specified
in the project architecture document (TODO.md §4.2).
"""

import json
from pathlib import Path

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for a specific CrewAI agent."""

    role: str = Field(..., description="Agent role title")
    goal: str = Field(..., description="Agent primary goal")
    backstory: str = Field(..., description="Agent backstory and persona")
    max_iter: int = Field(default=3, description="Maximum iterations for the agent")


def _load_configs() -> dict[str, AgentConfig]:
    config_file = Path(__file__).parent / "agents.json"
    if not config_file.exists():
        return {}
    with open(config_file, encoding="utf-8") as f:
        data = json.load(f)
    return {k: AgentConfig(**v) for k, v in data.items()}


AGENT_CONFIGS: dict[str, AgentConfig] = _load_configs()
