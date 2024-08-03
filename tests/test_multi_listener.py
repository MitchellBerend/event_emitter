from dataclasses import asdict, dataclass

import pytest

from event_emitter import EventSink
from event_emitter.utils import IsDataclass

LOG = []


@dataclass
class Foo:
    name: str
    age: int


class LogListener:
    @staticmethod
    def on() -> str:
        return "*"

    @classmethod
    def execute(cls, event: IsDataclass):
        LOG.append(asdict(event))


@pytest.fixture
def sink() -> EventSink:
    sink = EventSink()
    return sink


def test_multi_listener(sink: EventSink):
    sink.register_listener(LogListener)
    sink.register_listener(LogListener)

    foo = Foo(name="1", age=1)

    sink.emit(foo)
    sink.flush()

    assert len(LOG) == 2
