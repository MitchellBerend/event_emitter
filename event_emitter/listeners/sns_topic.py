import json
import os
import time
from dataclasses import asdict, is_dataclass
from typing import Self

import boto3

from event_emitter.utils import IsDataclass


def _prepare_sns_event(event_name: str, subject: str, event: IsDataclass):
    assert is_dataclass(event)

    id = f"{event_name}{time.time_ns()}"
    return {
        "Id": id,
        "Message": json.dumps(asdict(event)),
        "Subject": event_name,
        "MessageStructure": "string",
        "MessageDeduplicationId": id,
        "MessageGroupId": subject,
    }


class SNSListener:
    """
    This class acts as a listener for events and publishes them to an SNS topic.
    """

    __sns_topic = ""
    __sns_client = None

    def __new__(cls) -> Self:
        if cls.__sns_client is None or cls.__sns_topic == "":
            cls.__sns_client = boto3.client("sns")
            cls.__sns_topic = os.environ.get("SNS_TOPIC_ARN", "testARN")

        return cls.__instance  # type: ignore

    @staticmethod
    def on() -> str:
        """
        Returns the event type this listener is interested in.
        Returns '*' to indicate interest in all event types.

        Returns:
            str: The event type.
        """
        return "*"

    @classmethod
    def execute(cls, event: IsDataclass):
        """
        Executes the listener by publishing the event to the SNS topic.

        Args:
            event (IsDataclass): The event to be published. Must be a dataclass instance.
        """
        class_name = event.__class__.__name__
        message = _prepare_sns_event(class_name, class_name, event)
        message["TopicArn"] = cls.__sns_topic
        cls.__sns_client.publish(**message)  # type: ignore
