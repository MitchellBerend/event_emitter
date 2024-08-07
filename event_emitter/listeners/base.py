from typing import Protocol

from ..utils import IsDataclass


class ListenerBase(Protocol):
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

    def execute(self, event: IsDataclass):
        """
        Executes the listener's action when an event is emitted.

        Args:
            event (IsDataclass): The event to be processed. Must be a dataclass instance.
        """
        ...
