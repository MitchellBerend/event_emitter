from __future__ import annotations
from dataclasses import is_dataclass
from typing import List, Optional

from .listeners import ListenerBase
from .utils import IsDataclass


class EventSink:
    """
    This class acts as the main class of the event emitter library.

    This is the structure that wil be sent to a sns topic that is passed by an
    environment variable.
    {
       'Id': <Event type + timestamp>,
       'Message': <Your event>,
       'Subject': <Your subject>,
       'MessageStructure': 'string',
       'MessageDeduplicationId': <Event type + timestamp>,
       'MessageGroupId': <Your subject>
    },
    """

    __instance: Optional[EventSink] = None
    __events: List[IsDataclass] = []
    __listeners: List[ListenerBase] = []

    def __new__(cls) -> "EventSink":
        if cls.__instance is None:
            cls.__instance = super(EventSink, cls).__new__(cls)

        return cls.__instance  # type: ignore

    @classmethod
    def register_listener(cls, listener: ListenerBase):
        """
        Registers a listener to the EventSink. A listener decides what events it
        listens to by implementing the on() method.

        Args:
            listener (ListenerBase): The listener to be registered.
        """
        # Just making sure the instance exists
        if not cls.__instance:
            cls.__instance = cls()
        cls.__listeners.append(listener)

    @classmethod
    def emit(cls, event: IsDataclass):
        """
        Emits an event to the EventSink. The event is not sent unless flush() is
        called.

        Args:
            event (IsDataclass): The event to be emitted. Must be a dataclass instance.
        """
        # Just making sure the instance exists
        if not cls.__instance:
            cls.__instance = cls()
        assert is_dataclass(event)

        cls.__events.append(event)

    @classmethod
    def flush(cls):
        """
        Flushes all events in the EventSink and notifies all registered listeners.
        """
        # Just making sure the instance exists
        if not cls.__instance:
            cls.__instance = cls()

        for event in cls.__events:
            for listener in cls.__listeners:
                if listener.on() == "*" or listener.on() in event.__class__.__name__:
                    listener.execute(event)

        cls.__events = []
