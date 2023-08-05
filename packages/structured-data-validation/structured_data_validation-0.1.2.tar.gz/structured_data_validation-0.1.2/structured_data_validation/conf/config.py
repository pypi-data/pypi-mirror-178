"""
Summary: configuration helper module.

Configuration helper validation classes.
"""

from typing import Dict, List

from pydantic.dataclasses import dataclass


@dataclass
class Postgres:
    """Postgresql connection data class.

    Postgres connection arguments validation.
    """

    host: str
    username: str
    passwd: str
    port: int


@dataclass
class Parquet:
    """Parquet creation data class.

    Parquet data class.
    """

    partition_cols: List[str]
    compression: str


@dataclass
class Csv:
    """CSV dataclass.

    Csv data class for attribute validation.
    """

    json_cols: Dict[str, str]
