"""
Summary: Main script for AROS file validation.

To be modified.
"""

from datetime import timedelta
from timeit import default_timer as timer
from typing import List, Optional

from loguru import logger
import pandas as pd
from pyarrow import Table
import pyarrow.parquet as pq

from structured_data_validation.models.validate import (
    validate_AROS_file,
    validate_dataframe,
)


def write_dataframe_to_parquet_pyarrow(
    input_: pd.DataFrame, outfile: str, partition_cols: Optional[List[str]] = None
) -> None:
    """Write pandas.DataFrame in parquet format.

    Write pandas.DataFrame in parquet format.

    Args:
        input_: input pandas.DataFrame.
        outfile: output file path.
        partition_cols: list of columns to use for partitioning.

    """
    try:
        pq.write_to_dataset(
            Table.from_pandas(input_), root_path=outfile, partition_cols=partition_cols
        )
    except Exception as e:
        logger.exception(e)
    else:
        logger.success(f"Dataframe successfully written to: '{outfile}'.")


def output_validate(input_: str, output: Optional[str] = None) -> bool:
    """Validate the dataframe and write it to parquet file if provided.

    Args:
        input_: input file path.
        output: output file path.

    Returns:
        bool

    """
    start = timer()
    try:
        df = validate_AROS_file(input_)
    except Exception as e:
        logger.exception(e)
        return False
    else:
        if output is not None:
            write_dataframe_to_parquet_pyarrow(df, output)
        end = timer()
        logger.info(f"Elapsed time: {timedelta(seconds=end-start)}")
        return True


def main() -> None:
    """Respond to event and perform functionality.

    Main functionality.
    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input filename")
    parser.add_argument("--output", default=None, help="output filename")
    parser.add_argument("--schema", default="AROS", help="Only schema validation.")
    parser.add_argument(
        "--schema_only",
        default=False,
        action="store_true",
        help="Only schema validation.",
    )
    args = parser.parse_args()
    if args.schema_only:
        validate_dataframe(args.input, args.schema)
    else:
        output_validate(args.input, args.output)


if __name__ == "__main__":
    main()
