from typing import Any, ClassVar, Dict, Protocol


class IsDataclass(Protocol):
    # Checking for this attribute is the most reliable way to check if something
    # is a dataclass
    __dataclass_fields__: ClassVar[Dict[str, Any]]


class Listener(Protocol):
    """
    Protocol for event listeners. Any listener must implement these methods.
    """

    @staticmethod
    def on() -> str:
        """
        Specifies the event type this listener is interested in. The return
        string gets used to find exact matches on event names. A wildcard can be
        used to match on all events.

        Returns:
            str: The event type.
        """
        ...

    @classmethod
    def execute(cls, event: IsDataclass):
        """
        Executes the listener's action when an event is emitted.

        Args:
            event (IsDataclass): The event to be processed. Must be a dataclass instance.
        """
        ...
