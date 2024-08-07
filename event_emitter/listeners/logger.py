import logging
from dataclasses import asdict

from event_emitter.utils import IsDataclass


class DebugLogger:
    __LOGGER = None

    def __new__(cls) -> "DebugLogger":
        if cls.__LOGGER is None:
            cls.__LOGGER = logging.getLogger(__name__)

        return cls.__instance  # type: ignore

    @staticmethod
    def on() -> str:
        return "*"

    @classmethod
    def execute(cls, event: IsDataclass):
        assert isinstance(cls.__LOGGER, logging.Logger)
        class_name = event.__class__.__name__
        data = asdict(event)
        cls.__LOGGER.debug(f"{class_name}: {data}")
