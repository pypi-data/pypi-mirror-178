"""Module contains main cloud function.

To be modified soon.
# pip install --upgrade google-events
"""

import base64
import json
from typing import Dict, Optional, Tuple

import fastavro
from fastavro.validation import ValidationError
import functions_framework
from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient
from google.events.cloud.pubsub.v1 import MessagePublishedData
# from loguru import logger

from structured_data_validation.logging.gcp_logger import logger
from structured_data_validation.models.validate import (
    validate_dataframe,
    write_pandas_dataframe_to_parquet,
)


PROJECT_ID = "project_id"  # get these three parameters from config file.
TOPIC_ID = "topic_id"


def send_message_to_topic(
    record: Dict, project_id: str, topic_id: str, avsc_file: str
) -> None:
    """Send a message to a pubsub topic using Avro schema.

    Args:
        record (Dict): Message data in JSON format.
        project_id (str): ID of the project it belongs to.
        topic_id (str): PubSub Topic Id.
        avsc_file (str): Avro schema file in JSON format.
    """
    publisher_client = PublisherClient()
    topic_path = publisher_client.topic_path(project_id, topic_id)

    # Prepare to write Avro records to the binary output stream.
    # assert schema path.
    avro_schema = fastavro.schema.parse_schema(json.load(open(avsc_file)))
    try:
        _ = fastavro.validate(record, avro_schema)
    except ValidationError:
        logger.exception("Pubsub Topic Message Validation Error")
    else:
        try:
            future = publisher_client.publish(topic_path, record)
            result = future.result()
        except NotFound:
            logger.info(f"{topic_id} not found.")
        else:
            logger.info(f"Published message ID: {result}")


def main_pipe(
    data: Dict,
    partition_fields: Optional[Tuple] = ("analysis_type__name", "human__corporate_id"),
    schema: Optional[str] = "AROS",
) -> Dict:
    """AI is creating summary for main_pipe.

    Args:
        data (Dict): [description]
        partition_fields (Optional[Tuple], optional): [description].\
            Defaults to ("analysis_type__name", "human__corporate_id").
        schema (Optional[str], optional): [description].\
            Defaults to "AROS".

    Returns:
        Dict: [description]
    """
    input_ = data["file_name"]
    df = validate_dataframe(input_, schema)  # validation function
    try:
        write_pandas_dataframe_to_parquet(df, data["path"], list(partition_fields))
    except Exception as e:
        logger.exception(str(e))
        data['pipeline_status'] = 'failed'
        pass
    else:
        data['pipeline_status'] = 'succeeded'
    return data


def read_input_message(data: str) -> Dict:
    """Read input message and return as JSON string.

    Args:
        data (str): [description]

    Returns:
        Dict: [description]
    """
    return json.loads(base64.b64decode(data))


@functions_framework.cloud_event
def main(cloud_event: MessagePublishedData) -> None:
    """Process pubsub message, perform validation and write to output topic.

    Args:
        cloud_event (MessagePublishedData): [description]
    """
    data = read_input_message(cloud_event.data["message"]["data"])
    output_message = main_pipe(data)
    send_message_to_topic(output_message,
                          PROJECT_ID,
                          TOPIC_ID,
                          output_message["analysis_id"])
    logger.info("Successfully executed!")
