"""
Summary: base module for custom models.

Initial implementation to fit Analysis and Experiment models.
"""

from typing import Any, Dict, Optional, Tuple

import pandas as pd
from pydantic import BaseModel

from structured_data_validation.models.datatypes import EmptyEnum


class ModifiedBaseModel(BaseModel):
    """Modified Base Model which allows non registered attributes\
    in the model to be included.

    This implementation FORCE NON REGISTERED ATTRIBUTES VALUES
    TO CASTED INTO STRINGS.
    The reason for that to happen is to avoid issues with schemas
    in file formats like parquet, ...

    Args:
        BaseModel (BaseModel): parent class.
    """

    def __init__(__pydantic_self__, **data: Dict) -> None:
        """Perform non-registered attributes registry in the model.

        Perform non-registered attributes registry in the model\
        which allows extra arguments.

        Args:
            **data: named arguments for model.
        """
        registered, not_registered = __pydantic_self__.filter_data(data)
        super().__init__(**registered)
        for key, val in not_registered.items():
            __pydantic_self__.__dict__[key] = (
                str(val) if val is not None else None
            )  # Turn values to string, log not_registered attributes.

    @classmethod
    def filter_data(cls, data: Dict) -> Tuple[Dict[Any, Any]]:
        """Filter data attributes.

        Filter canonical and non-canonical attributes.

        Args:
            data (Dict): arguments Dictionary.

        Returns:
            Tuple (Dict): tuple of arguments.
        """
        registered_attr = {}
        not_registered_attr = {}
        annots = cls.__annotations__
        for k, v in data.items():
            if k in annots:
                registered_attr[k] = cls.standarize_empty_null_str_values(v)
            else:
                not_registered_attr[k] = cls.standarize_empty_null_str_values(v)
        return registered_attr, not_registered_attr

    @classmethod
    def standarize_empty_null_str_values(cls, value: Optional[str]) -> Optional[str]:
        """Standardize empty and Null attributes.

        If value in Enum return None, else value or None.

        Args:
            value: provided value.

        Returns:
            Optional (str): either string or None.
        """
        if isinstance(value, str):
            if not len(value.strip()):
                value = None
            elif value.upper() in [i.value for i in EmptyEnum.__members__.values()]:
                value = None
        elif pd.isna(value):
            value = None
        return value
