from logging import Logger, getLogger
from dataclasses import asdict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from event_emitter import IsDataclass


class DebugLogger:
    def __init__(self, on: str = "*"):
        self.__LOGGER = getLogger(__name__)
        self.__on = on

    def on(self) -> str:
        return self.__on

    def execute(self, event: "IsDataclass"):
        assert isinstance(self.__LOGGER, Logger)
        class_name = event.__class__.__name__
        data = asdict(event)
        self.__LOGGER.debug(f"{class_name}: {data}")
