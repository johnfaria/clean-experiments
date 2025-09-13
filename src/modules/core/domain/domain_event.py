"""Domain event base class module.

This module defines the base DomainEvent class that all domain events
should inherit from, providing common event properties and structure.
"""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from bson import ObjectId


@dataclass(frozen=True)
class DomainEvent(ABC):
    """Base class for all domain events.

    Represents something important that happened in the domain
    that other parts of the system might be interested in.

    Attributes:
        aggregate_id: The ID of the aggregate that generated this event.
        occurred_at: When the event occurred.
        event_version: Version of the event schema for evolution support.
    """

    aggregate_id: ObjectId
    occurred_at: datetime
