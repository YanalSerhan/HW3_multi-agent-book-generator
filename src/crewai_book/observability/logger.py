import sys
from typing import Any

from loguru import logger

from ..config.settings import settings


def setup_logger() -> None:
    """Configure loguru with structured logging and appropriate levels."""
    logger.remove()  # Remove default handler

    # Base format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # If in development, output to console with colors
    log_level = "DEBUG" if settings.app_env == "development" else "INFO"

    logger.add(sys.stderr, format=log_format, level=log_level, colorize=True, enqueue=True)

    # File logging for all environments
    logger.add(
        "output/logs/app_{time}.log",
        format="{time} | {level} | {name}:{function}:{line} | {extra} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        enqueue=True,
        serialize=True,  # JSON structured logs for files
    )


def get_logger(module_name: str) -> Any:
    """Get a contextualized logger."""
    return logger.bind(module=module_name)
