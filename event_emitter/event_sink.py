from dataclasses import is_dataclass
from typing import List, Self

from .utils import IsDataclass, Listener


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

    __instance: Self | None = None
    __events: List[IsDataclass] = []
    __listeners: List[Listener] = []

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super(EventSink, cls).__new__(cls)

        return cls.__instance  # type: ignore

    @classmethod
    def register_listener(cls, listener: Listener):
        """
        Registers a listener to the EventSink. A listener decides what events it
        listens to by implementing the on() method.

        Args:
            listener (Listener): The listener to be registered.
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

        for listener in cls.__listeners:
            for event in cls.__events:
                if listener.on() in event.__class__.__name__ or listener.on() == "*":
                    listener.execute(event)

        cls.__events = []
