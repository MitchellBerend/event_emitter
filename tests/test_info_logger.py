from dataclasses import dataclass, asdict
import logging
from unittest.mock import patch, MagicMock

import pytest

from event_emitter import InfoLogger, ListenerBase


@dataclass
class Foo:
    name: str
    age: int


@pytest.fixture(autouse=True)
def reset_singleton():
    InfoLogger._InfoLogger__logger = None  # type: ignore
    InfoLogger._InfoLogger__instance = None  # type: ignore


def test_implements_protocol():
    assert issubclass(InfoLogger, ListenerBase)


def test_info_on():
    assert InfoLogger().on() == "*"
    assert InfoLogger("Foo").on() == "Foo"


@patch("event_emitter.listeners.info_logger.getLogger")
def test_execute(mock_get_logger):
    mock_logger = MagicMock(spec=logging.Logger)
    mock_get_logger.return_value = mock_logger

    event = Foo(name="test", age=42)

    logger = InfoLogger()
    logger.execute(event)

    class_name = event.__class__.__name__
    data = asdict(event)

    mock_logger.info.assert_called_once_with(f"{class_name}: {data}")
