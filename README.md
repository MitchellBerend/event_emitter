# Event Emitter Library

## Overview

This library provides a simple framework for emitting and handling events in a
Python application. The primary components are `Listener`, a protocol that
defines the interface for event listeners, and `EventSink`, a singleton class
that manages event emission and listener notification.

## Components

### Listener Protocol

The `Listener` protocol defines two essential methods that any event listener
must implement:

- `on() -> str`: Specifies the type of event the listener is interested in. This
  method returns a string that is used to match events. It can return a specific
  event type or a wildcard (`*`) to match all events.

- `execute(cls, event: IsDataclass)`: Executes the listener's action when an
  event is emitted. This method takes an event, which must be an instance of a
  dataclass.

### EventSink Class

The `EventSink` class manages the registration of listeners and the emission of
events. It ensures that events are only processed after they are flushed,
providing a batched handling mechanism.

#### Methods

- `register_listener(cls, listener: Listener)`: Registers a listener to the
  `EventSink`.
- `emit(cls, event: IsDataclass)`: Emits an event to the `EventSink`. The event
  is added to the event list.
- `flush(cls)`: Flushes all events and notifies all registered listeners.

## Usage

### Defining a Listener

To create a listener, define a class that implements the `Listener` protocol:

```python
from dataclasses import dataclass

@dataclass
class MyEvent:
    data: str

class MyListener:
    @staticmethod
    def on() -> str:
        return "MyEvent"

    @classmethod
    def execute(cls, event: MyEvent):
        print(f"Event received: {event.data}")
```

### Registering a Listener

Register the listener with the `EventSink`:

```python
EventSink.register_listener(MyListener)
```

### Emitting an Event

Emit an event:

```python
event = MyEvent(data="Hello, World!")
EventSink.emit(event)
```

### Flushing Events

Flush the events to notify all listeners:

```python
EventSink.flush()
```

### Example

Here's a complete example of defining a listener, registering it, emitting an
event, and flushing the events:

```python
from dataclasses import dataclass

@dataclass
class MyEvent:
    data: str

class MyListener:
    @staticmethod
    def on() -> str:
        return "MyEvent"

    @classmethod
    def execute(cls, event: MyEvent):
        print(f"Event received: {event.data}")

# Register the listener
EventSink.register_listener(MyListener)

# Emit an event
event = MyEvent(data="Hello, World!")
EventSink.emit(event)

# Flush the events
EventSink.flush()
```

In this example, `MyListener` will receive and process the `MyEvent` when
`EventSink.flush()` is called, printing "Event received: Hello, World!".

## Notes

- Ensure that the events emitted are instances of dataclasses.
- The `Listener` protocol's `on` method can return a wildcard (`*`) to match all
  events.
- The `EventSink` ensures that events are only processed after they are flushed,
  providing a batched handling mechanism.
