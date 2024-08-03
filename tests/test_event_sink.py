from dataclasses import dataclass

import pytest

from event_emitter import EventSink


@dataclass
class Foo:
    name: str
    age: int


@pytest.fixture
def sink() -> EventSink:
    sink = EventSink()
    return sink


def test_events(sink: EventSink):
    for i in range(10):
        foo = Foo(name=str(i), age=i)
        sink.emit(foo)

    assert len(sink._EventSink__events) == 10  # type: ignore
    sink.flush()


def test_singleton_instance():
    instance1 = EventSink()
    instance2 = EventSink()
    assert instance1 is instance2
