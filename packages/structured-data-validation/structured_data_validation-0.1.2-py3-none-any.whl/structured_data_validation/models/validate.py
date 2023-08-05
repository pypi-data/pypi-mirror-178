"""
Summary: validate models.

Functions to perform model validation.
"""

import importlib
import json
from typing import Callable, Dict, Generator, List, Optional

from loguru import logger
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from structured_data_validation.models.AROS import AROS


DATAFRAME_JSON_FIELDS = {
    "experiment_result.data": "analysis_type.name",
    "analysis_result.data": "analysis_type.name",
}


def validate_data_schema(data_schema: ModelMetaclass) -> Callable:
    """Add validation functionality to dataframes.

    Args:
        data_schema (ModelMetaclass): [description]

    Returns:
        Callable: [description]
    """

    def Inner(func: Callable) -> Callable:
        """Create wrapper function.

        Args:
            func (Callable): [description]

        Returns:
            Callable: [description]
        """

        def wrapper(*args: List, **kwargs: Dict) -> pd.DataFrame:
            """Perform function call on arguments.

            Perform function call on arguments.

            Args:
                args: extra arguments list.
                kwargs: named extra arguments dict.

            Raises:
                TypeError: [description]

            Returns:
                pd.DataFrame: [description]
            """
            res = func(*args, **kwargs)
            if isinstance(res, pd.DataFrame):
                # check result of the function execution against the data_schema
                df_dict = res.to_dict(orient="records")

                # Wrap the data_schema into a helper class for validation
                class ValidationWrap(BaseModel):
                    df_dict: List[data_schema]

                # Do the validation
                _ = ValidationWrap(df_dict=df_dict)
            else:
                raise TypeError(
                    "Provided function is not returning \
                    an object of type pandas.DataFrame."
                )

            return res

        return wrapper

    return Inner


def dataframe_validation(df: pd.DataFrame, schema: str) -> pd.DataFrame:
    """Validate dataframes.

    Args:
        df (pd.DataFrame): input pandas.DataFrame.
        schema (str): schema name to be used.

    Returns:
        pd.DataFrame: validated pandas.DataFrame.
    """
    cls = getattr(
        importlib.import_module(f"structured_data_validation.models.{schema}"), schema
    )

    @validate_data_schema(data_schema=cls)
    def validate_dataframe(df_: pd.DataFrame) -> pd.DataFrame:
        """Perform dataframe schema validation.

        Perform dataframe schema validation.

        Args:
            df_: input pandas.Dataframe

        Returns:
            pandas.DataFrame

        """
        return df_

    return validate_dataframe(df)


def validate_dataframe(input: str, schema: str) -> None:
    """Perform pandas.DataFrame validation.

    Perform pandas.DataFrame validation.

    Args:
        input (str): [description]
        schema (str): [description]
    """
    df = pd.DataFrame(list(svv_csv_pandas_reader(input)))
    _ = dataframe_validation(df, schema)
    logger.info(f"File was successfully validated against '{schema}' schema.")


def svv_csv_pandas_reader(
    filename: str, json_fields: Dict[str, str] = DATAFRAME_JSON_FIELDS
) -> Generator:
    """Read and parse AROS csv file.

    Args:
        filename (str): [description]
        json_fields (Dict[str, str], optional): JSON fields in data structure.\
            Defaults to DATAFRAME_JSON_FIELDS.

    Yields:
        Generator: [description]
    """
    keys = json_fields.keys()
    df = pd.read_csv(filename)
    for row_dict in df.to_dict(orient="records"):
        for key in row_dict.keys():
            if key in keys:
                # data = {k: str(v) for k,v in json.loads(row_dict[key]).items()}
                # This is done at validation class level for not described attributes.
                data = json.loads(row_dict[key])
                row_dict[key] = data
                row_dict[key][json_fields[key].replace(".", "__")] = row_dict[
                    json_fields[key]
                ]
        yield row_dict


def validate_AROS_file(
    input: str,
    model: Optional[ModelMetaclass] = AROS,
    json_fields: Optional[Dict[str, str]] = DATAFRAME_JSON_FIELDS,
) -> Optional[pd.DataFrame]:
    """Validate AROS csv file.

    Args:
        input (str): Input file path.
        model (ModelMetaclass, optional): ModelMetaclass. Defaults to AROS.
        json_fields (Dict[str, str], optional): JSON fields in data structure.\
            Defaults to DATAFRAME_JSON_FIELDS.

    Returns:
        pd.DataFrame: [description]
    """
    try:
        df = pd.DataFrame(
            [
                json.loads(model(**row).json())
                for row in svv_csv_pandas_reader(input, json_fields=json_fields)
            ]
        )
    except Exception as e:
        logger.exception(e)
        df = None
    else:
        logger.success(f"Successfully validated file '{input}'.")
    return df


def write_pandas_dataframe_to_parquet(
    df: pd.DataFrame, output: str, partition_fields: List[str]
) -> None:
    """Write pandas.DataFrame to parquet.

    Write pandas.DataFrame to parquet.

    Args:
        df (pd.DataFrame): input pandas.Dataframe.
        output (str): output path.
        partition_fields (List[str]): list of field names for partitioning.
    """
    try:
        table = pa.Table.from_pandas(df)
        pq.write_to_dataset(
            table,
            root_path=output,
            partition_cols=partition_fields,
        )
    except Exception as e:
        logger.exception(str(e))
    else:
        logger.success(f"Output file was written to: {output}.")
