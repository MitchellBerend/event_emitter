from dataclasses import dataclass

import pytest

import event_emitter
from event_emitter import EventSink, ListenerBase


@dataclass
class Bar:
    name: str
    age: int


@dataclass
class Baz:
    name: str
    lastname: str
    age: int


class FitleredExcludedListener:
    @staticmethod
    def on() -> str:
        """This tests if the filter mechanism on the EventSink actually works"""
        return "NotBar"

    def execute(self: ListenerBase, event: event_emitter.utils.IsDataclass):
        LOG.append(event)


class FitleredIncludedListener:
    @staticmethod
    def on() -> str:
        """This also tests if the filter mechanism on the EventSink actually works"""
        return "Baz"

    def execute(self: ListenerBase, event: event_emitter.utils.IsDataclass):
        LOG.append(event)


LOG = []
SINK = EventSink()
SINK.register_listener(FitleredExcludedListener())
SINK.register_listener(FitleredIncludedListener())


@pytest.fixture
def sink() -> EventSink:
    return SINK


def test_events_filter_exclude(sink: EventSink):
    for i in range(10):
        sink.emit(Bar(name=str(i), age=i))

    assert len(sink._EventSink__events) == 10  # type: ignore
    sink.flush()
    assert len(sink._EventSink__events) == 0  # type: ignore
    assert len(LOG) == 0


def test_events_filter_include(sink: EventSink):
    for i in range(5):
        sink.emit(Bar(name=str(i), age=i))
        sink.emit(Baz(name=str(i), lastname=str(i + 1), age=i))

    assert len(sink._EventSink__events) == 10  # type: ignore
    sink.flush()
    assert len(sink._EventSink__events) == 0  # type: ignore
    assert len(LOG) == 5


def test_singleton_instance():
    instance1 = EventSink()
    instance2 = EventSink()
    assert instance1 is instance2
