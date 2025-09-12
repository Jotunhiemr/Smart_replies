# type: ignore
import logging
from config import config


def setup_logging(level: int = None) -> logging.Logger:
    """
    Configure logging with proper formatting

    Args:
        level: Logging level (defaults to config.LOG_LEVEL)

    Returns:
        Logger instance
    """
    if level is None:
        level = config.LOG_LEVEL

    logging.basicConfig(
        level=level,
        format=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    return logging.getLogger(__name__)


def security():
    pass
