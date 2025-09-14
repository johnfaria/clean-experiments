"""Domain entity base class with identity and domain event support."""

from dataclasses import dataclass, field
from typing import override

from bson import ObjectId

from .domain_event import DomainEvent


@dataclass
class Entity:
    """Base class for domain entities with identity and domain event support.

    Entities are distinguished by their identity (UUID) rather than their attributes.
    Two entities with the same ID are considered equal, even if their other attributes differ.

    This base class provides:
    - Automatic ObjectId generation for entity identity
    - Domain event collection and management
    - Proper equality and hashing based on identity

    Attributes:
        id: Unique identifier for the entity, automatically generated
        _domain_events: Internal list of domain events to be dispatched

    Example:
        ```python
        @dataclass
        class User(Entity):
            name: str
            email: str

        user = User(name="John", email="john@example.com")
        user.add_domain_event(UserCreatedEvent(user.id))
        ```
    """

    id: ObjectId = field(default_factory=ObjectId, init=False)
    _domain_events: list[DomainEvent] = field(default_factory=list, init=False)

    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to be dispatched later.

        Domain events represent something important that happened in the domain.
        They are collected here and typically dispatched by an event dispatcher
        after the entity changes are persisted.

        Args:
            event: The domain event to add to the collection

        Example:
            ```python
            user = User(name="John", email="john@example.com")
            user.add_domain_event(UserCreatedEvent(user.id, user.name))
            ```
        """
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Clear all domain events.

        This is typically called after domain events have been successfully
        dispatched to prevent them from being dispatched multiple times.

        Example:
            ```python
            # After persisting entity and dispatching events
            user.clear_domain_events()
            ```
        """
        self._domain_events.clear()

    @property
    def domain_events(self) -> list[DomainEvent]:
        """Get a copy of all domain events.

        Returns a copy to prevent external modification of the internal
        event collection. Use add_domain_event() to add new events.

        Returns:
            A copy of all domain events currently collected

        Example:
            ```python
            events = user.domain_events
            for event in events:
                event_dispatcher.dispatch(event)
            user.clear_domain_events()
            ```
        """
        return self._domain_events.copy()

    @override
    def __eq__(self, other: object) -> bool:
        """Check equality based on entity identity.

        Two entities are equal if they are of the same type and have the same ID.
        This implements the DDD concept that entities are distinguished by identity,
        not by their attributes.

        Args:
            other: Object to compare with

        Returns:
            True if both entities have the same type and ID, False otherwise

        Example:
            ```python
            user1 = User(name="John", email="john@example.com")
            user2 = User(name="Jane", email="jane@example.com")
            user2.id = user1.id  # Same ID
            assert user1 == user2  # True, despite different attributes
            ```
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    @override
    def __hash__(self) -> int:
        """Generate hash based on entity identity.

        The hash is based solely on the entity's ID, ensuring that entities
        with the same identity have the same hash value, making them suitable
        for use in sets and as dictionary keys.

        Returns:
            Hash value based on the entity's ID

        Example:
            ```python
            user = User(name="John", email="john@example.com")
            user_set = {user}  # Can be used in sets
            user_dict = {user: "some_value"}  # Can be used as dict keys
            ```
        """
        return hash(self.id)
