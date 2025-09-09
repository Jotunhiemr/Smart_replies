import logging
from config import Config


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(Config.LOG_LEVEL)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(Config.LOG_LEVEL)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger