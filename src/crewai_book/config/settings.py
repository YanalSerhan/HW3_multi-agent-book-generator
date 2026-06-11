import json
from pathlib import Path
from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def _load_json_config(file_path: Path) -> dict[str, Any]:
    """Load JSON config file safely."""
    if file_path.exists():
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    return {}


class AppSettings(BaseSettings):
    """Application-wide settings loaded from .env and config files."""

    # API Keys
    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")
    serper_api_key: SecretStr = Field(default=SecretStr(""), alias="SERPER_API_KEY")

    # App Config
    app_env: str = Field(default="production", alias="APP_ENV")
    human_review_outline: bool = Field(default=True, alias="HUMAN_REVIEW_OUTLINE")
    human_review_draft: bool = Field(default=True, alias="HUMAN_REVIEW_DRAFT")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class ConfigManager:
    """Manager to load static JSON configurations."""

    def __init__(self) -> None:
        """Initialize."""
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.setup_config = _load_json_config(self.config_dir / "settings.json")
        self.rate_limits_config = _load_json_config(self.config_dir / "rate_limits.json")

    def get_setup(self) -> dict[str, Any]:
        """Get the general setup configuration."""
        return self.setup_config

    def get_rate_limits(self) -> dict[str, Any]:
        """Get the rate limits configuration."""
        return self.rate_limits_config


# Global instances
config_manager = ConfigManager()
settings = AppSettings()  # type: ignore
