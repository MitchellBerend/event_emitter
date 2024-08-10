from dataclasses import dataclass, asdict
import logging
from unittest.mock import patch, MagicMock

import pytest

from event_emitter import DebugLogger, ListenerBase


@dataclass
class Foo:
    name: str
    age: int


@pytest.fixture(autouse=True)
def reset_singleton():
    DebugLogger._DebugLogger__LOGGER = None  # type: ignore
    DebugLogger._DebugLogger__instance = None  # type: ignore


def test_implements_protocol():
    assert issubclass(DebugLogger, ListenerBase)


def test_debug_on():
    assert DebugLogger().on() == "*"
    assert DebugLogger("Foo").on() == "Foo"


@patch("event_emitter.listeners.debug_logger.getLogger")
def test_execute(mock_get_logger):
    mock_logger = MagicMock(spec=logging.Logger)
    mock_get_logger.return_value = mock_logger

    event = Foo(name="test", age=42)

    logger = DebugLogger()
    logger.execute(event)

    class_name = event.__class__.__name__
    data = asdict(event)

    mock_logger.debug.assert_called_once_with(f"{class_name}: {data}")
