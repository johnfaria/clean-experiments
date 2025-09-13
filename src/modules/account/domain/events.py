"""User domain events module.

This module defines domain events specific to the User aggregate,
representing important business events that occur during user operations.
"""

from dataclasses import dataclass
from datetime import datetime

from bson import ObjectId
from src.modules.core.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class UserCreated(DomainEvent):
    """Event raised when a new user is created.

    This event captures the initial state of a user when they are
    first created in the system.

    Attributes:
        name: The user's name.
        email: The user's email address.
        age: The user's age.
    """

    name: str
    email: str
    age: int

    @classmethod
    def create(
        cls, aggregate_id: ObjectId, name: str, email: str, age: int
    ) -> "UserCreated":
        """Create a UserCreated event with current timestamp.

        Args:
            aggregate_id: The unique identifier of the user aggregate.
            name: The user's name.
            email: The user's email address.
            age: The user's age.

        Returns:
            UserCreated: The created domain event instance.
        """
        return cls(
            aggregate_id=aggregate_id,
            occurred_at=datetime.now(),
            name=name,
            email=email,
            age=age,
        )


@dataclass(frozen=True)
class UserEmailChanged(DomainEvent):
    """Event raised when a user's email address is changed.

    This event captures both the old and new email addresses
    for audit and notification purposes.

    Attributes:
        old_email: The previous email address.
        new_email: The new email address.
    """

    old_email: str
    new_email: str

    @classmethod
    def create(
        cls, aggregate_id: ObjectId, old_email: str, new_email: str
    ) -> "UserEmailChanged":
        """Create a UserEmailChanged event with current timestamp.

        Args:
            aggregate_id: The unique identifier of the user aggregate.
            old_email: The previous email address.
            new_email: The new email address.

        Returns:
            UserEmailChanged: The created domain event instance.
        """
        return cls(
            aggregate_id=aggregate_id,
            occurred_at=datetime.now(),
            old_email=old_email,
            new_email=new_email,
        )
