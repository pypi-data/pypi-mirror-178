"""Formatter logging module.

Improvements coming soon.
"""

import sys
from typing import Dict

from loguru import logger


class Formatter:
    """Fomatter class.

    Example of formatter class.
    """

    def __init__(self) -> None:
        """Initialise class attribute values."""
        self.padding = 0
        self.fmt = "{time} | {level: <8} | \
            {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

    def format(self, record: Dict) -> str:
        """Adjust the padding length dinamically \
        based on previously encountered values.

        Args:
            record (Dict): [description]

        Returns:
            str: [description]
        """
        length = len("{name}:{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


formatter = Formatter()

logger.remove()
logger.add(sys.stderr, format=formatter.format)
