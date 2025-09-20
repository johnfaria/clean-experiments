"""Event dispatcher module.

This module provides infrastructure for dispatching domain events
to registered handlers, enabling decoupled event-driven architecture.
"""

from typing import Protocol

from src.modules.core.domain.domain_event import DomainEvent


class EventHandler(Protocol):
    """Protocol for event handlers.

    Event handlers must implement the handle method to process
    domain events they are interested in.
    """

    def handle(self, event: DomainEvent) -> None:
        """Handle a domain event.

        Args:
            event: The domain event to handle.
        """
        ...


class EventDispatcher:
    """Dispatches domain events to registered handlers.

    Provides a simple publish-subscribe mechanism for domain events,
    allowing multiple handlers to react to the same event.
    """

    def __init__(self) -> None:
        """Initialize the event dispatcher."""
        self._handlers: dict[type[DomainEvent], list[EventHandler]] = {}

    def subscribe(self, event_type: type[DomainEvent], handler: EventHandler) -> None:
        """Subscribe a handler to an event type.

        Args:
            event_type: The type of event to subscribe to.
            handler: The handler that will process the event.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def dispatch(self, events: list[DomainEvent]) -> None:
        """Dispatch a list of events to their registered handlers.

        Args:
            events: List of domain events to dispatch.
        """
        print(f"Dispatching {len(events)} events")
        for event in events:
            handlers = self._handlers.get(type(event), [])
            for handler in handlers:
                handler.handle(event)

    def dispatch_single(self, event: DomainEvent) -> None:
        """Dispatch a single event to its registered handlers.

        Args:
            event: The domain event to dispatch.
        """
        self.dispatch([event])

    def clear_handlers(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()

    def get_handler_count(self, event_type: type[DomainEvent]) -> int:
        """Get the number of handlers registered for an event type.

        Args:
            event_type: The event type to check.

        Returns:
            The number of registered handlers.
        """
        return len(self._handlers.get(event_type, []))
