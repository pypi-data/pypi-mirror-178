"""Handler module.

To be improved soon.
"""

import traceback
from typing import Optional

import google.cloud.logging
from google.events.cloud.pubsub.v1 import MessagePublishedData
from loguru import logger


HANDLER_NAME = "GCP Handler"


class StackDriverSink:
    """Handler for GCP structured logging."""

    def __init__(self, logger_name: Optional[str] = HANDLER_NAME) -> None:
        """Initialize object on instantiation.

        Args:
            logger_name (str, optional): [description]. Defaults to HANDLER_NAME.
        """
        self.logging_client = google.cloud.logging.Client()
        self.logger = self.logging_client.logger(logger_name)

    def write(self, message: MessagePublishedData) -> None:
        """Write message to log.

        Args:
            message (MessagePublishedData): [description]
        """
        record = message.record
        log_info = {
            "elapsed": {
                "microseconds": record["elapsed"] // record["elapsed"].resolution,
                "seconds": record["elapsed"].total_seconds(),
            },
            "exception": (
                None
                if record["exception"] is None
                else "".join(
                    traceback.format_exception(
                        None, record["exception"].value, record["exception"].traceback
                    )
                )
            ),
            "message": record["message"],
            "module": record["module"],
            "name": record["name"],
            "process": {"id": record["process"].id, "name": record["process"].name},
            "thread": {"id": record["thread"].id, "name": record["thread"].name},
            "extra": {
                k: str(v)
                for k, v in record["extra"].items()
                if "record" not in record["extra"]
            },
        }
        self.logger.log_struct(
            log_info,
            severity=record["level"].name,
            source_location={
                "file": record["file"].name,
                "function": record["function"],
                "line": record["line"],
            },
        )


logger.add(StackDriverSink())
