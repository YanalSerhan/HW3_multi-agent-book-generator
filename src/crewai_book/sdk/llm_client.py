from typing import Any

import httpx

from ..config.settings import settings
from ..exceptions.domain import APIConnectionError
from ..shared.gatekeeper import ApiGatekeeper
from .base import BaseClient


class LLMClient(BaseClient):
    """Client for interacting with LLM APIs via httpx."""

    def __init__(self, gatekeeper: ApiGatekeeper | None = None) -> None:
        """Initialize."""
        super().__init__("openai", gatekeeper)
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {settings.openai_api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }

    def _sync_post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Synchronous POST request to OpenAI API."""
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.base_url}/{endpoint}", json=payload, headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return data if isinstance(data, dict) else {}
        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error during LLM call: {e}")
            raise APIConnectionError("LLM API call failed", {"error": str(e)}) from e

    def complete(
        self, messages: list[dict[str, Any]], model: str = "gpt-4o", temperature: float = 0.7
    ) -> str:
        """Get a completion from the LLM."""
        payload = {"model": model, "messages": messages, "temperature": temperature}

        response_data = self._execute(self._sync_post, "chat/completions", payload)

        try:
            return str(response_data["choices"][0]["message"]["content"])
        except (KeyError, IndexError) as e:
            self.logger.error(f"Malformed LLM response: {response_data}")
            raise APIConnectionError("Malformed LLM response") from e
