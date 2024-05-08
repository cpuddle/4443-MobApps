# log_config.py
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    # Create logs directory if it does not exist
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Logging configuration
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    LOGGING_LEVEL = logging.INFO

    logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)
    logger = logging.getLogger("uvicorn.error")

    # Add a rotating file handler to log error messages to a file
    handler = RotatingFileHandler("logs/error.log", maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(handler)

    return logger
