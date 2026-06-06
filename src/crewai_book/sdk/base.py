from collections.abc import Callable
from typing import Any

from ..observability.logger import get_logger
from ..shared.gatekeeper import ApiGatekeeper


class BaseClient:
    """Base class for all SDK clients providing common dependencies."""

    def __init__(
        self, service_name: str, gatekeeper: ApiGatekeeper | None = None
    ) -> None:
        self.service_name = service_name
        self.logger = get_logger(f"sdk.{service_name}")
        self.gatekeeper = gatekeeper or ApiGatekeeper(service_name)

    def _execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute a function through the gatekeeper."""
        self.logger.debug(f"Executing call to {self.service_name}")
        return self.gatekeeper.execute(func, *args, **kwargs)
