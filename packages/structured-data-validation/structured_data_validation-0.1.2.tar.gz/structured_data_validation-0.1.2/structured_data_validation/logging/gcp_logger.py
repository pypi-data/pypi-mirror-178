"""GCP simple logging function.

Improvements to come soon.
"""

import json
import sys
from typing import Dict

from loguru import logger


def serialize(record: Dict) -> str:
    """Serialize logging records.

    Args:
        record (Dict): [description]

    Returns:
        str: [description]
    """
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
    }
    return json.dumps(subset)


def patching(record: Dict) -> None:
    """Patch logger object.

    Args:
        record (Dict): [description]
    """
    record["extra"]["serialized"] = serialize(record)


logger.remove(0)

logger = logger.patch(patching)
logger.add(sys.stderr, format="{extra[serialized]}")
