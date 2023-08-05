"""
Logging module.

It provides convenience functionality for logging.
"""

import sys
from typing import Optional

import loguru


def get_logger(
    log_file: str = "log.txt",
    log_format: Optional[str] = (
        "<blue>{elapsed.seconds:0>4}s</blue> |"
        " <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> |"
        " <level>{level: <8}</level> | "
        " <cyan>{name}:{function}</cyan>:<cyan>{line}</cyan>"
        " - <level>{message}</level>"
    ),
    logger_: loguru.logger.Logger = loguru.logger,
) -> loguru.logger.Logger:
    """Get custom logger function.

    Custom log from loguru.

    Args:
        log_file (str): file to log to.
        log_format (str, optional): pattern for log format.
        logger_ (loguru._logger.Logger, optional): Defaults to logger.

    Returns:
        loguru._logger.Logger: Logger from loguru.
    """
    logger_.remove()  # remove default logger
    logger_.add(sys.stderr, format=log_format)
    logger_.add(log_file, format=log_format)  # log to a file as well
    logger_ = logger_.opt(colors=True)
    return logger_
