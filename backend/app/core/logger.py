# proper logging.


import os
import sys
from pathlib import Path
from loguru import logger
from datetime import timedelta, timezone
from typing import Optional

# Define the logs directory and ensure it exists using pathlib
LOGS_DIR = "logs"
log_path = Path(LOGS_DIR) / "guardflow.log"

if not log_path.parent.exists():
    log_path.parent.mkdir(parents=True)

def configure_logger() -> None:
    """
    Configures the logger with console and file handlers.

    The logger is configured to output logs to both the console and a file.
    - File logging is done in `logs/guardflow.log` with daily rotation, 30-day retention, ZIP compression,
      and an enqueue strategy for performance improvements.
    - Console logging is set up to only display INFO level messages.

    Args:
        None

    Returns:
        None
    """
    # Configure file handler
logger.add(
        log_path,
    rotation="1 day",
        retention=None,
    compression="zip",
    serialize=False,
    enqueue=True,
    backtrace=True,
    diagnose=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}.{function}:{line} | {message}",
)

    # Configure console handler
logger.add(
    "sys.stdout",
    rotation="1 day",
        retention=None,
    compression="zip",
    serialize=False,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    filter=lambda record: record["level"].name == "INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}.{function}:{line} | {message}",
)

# Call the configure_logger function to set up the logger
configure_logger()

# Export the configured logger
guardflow_logger = logger

# Example usage of the global logger
if __name__ == "__main__":
    guardflow_logger.info("This is an info message")
    logger.add(
        sys.stdout,
        rotation="1 day",
        retention=timedelta(days=30),
        compression="zip",
        serialize=False,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        filter=lambda record: record["level"].name == "INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}.{function}:{line} | {message}",
    )

# Call the configure_logger function to set up the logger
configure_logger()

# Export the configured logger
guardflow_logger = logger

# Example usage of the global logger
if __name__ == "__main__":
    guardflow_logger.info("This is an info message")