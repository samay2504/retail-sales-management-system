"""Structured JSON logging configuration."""

import logging
import sys
from pythonjsonlogger import jsonlogger

from src.config import settings


def setup_logging() -> None:
    """Configure structured JSON logging."""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    if settings.log_format == "json":
        # JSON formatter
        formatter: logging.Formatter = jsonlogger.JsonFormatter(  # type: ignore[assignment]
            "%(timestamp)s %(level)s %(name)s %(message)s %(request_id)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"},
        )
    else:
        # Standard formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
