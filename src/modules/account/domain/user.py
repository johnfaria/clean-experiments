"""User domain entity module.

This module defines the User entity with core user attributes and business
logic for user-related operations such as age validation.
"""

from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID

from src.modules.core.domain.entity import Entity
from src.modules.account.domain.value_objects.name import Name
from src.modules.account.domain.value_objects.age import Age
from src.modules.account.domain.value_objects.email import Email
from src.modules.account.domain.events import UserCreated, UserEmailChanged


class UserProperties(TypedDict):
    """Properties for creating or restoring a User."""

    name: str
    age: int
    email: str


@dataclass(unsafe_hash=True)
class User(Entity):
    """Represents a user in the system.

    A rich domain entity containing value objects for name, age, and email
    with encapsulated validation logic.

    Attributes:
        name: The user's name as a Name value object.
        age: The user's age as an Age value object.
        email: The user's email as an Email value object.
    """

    name: Name
    age: Age
    email: Email

    @classmethod
    def create(cls, properties: UserProperties) -> "User":
        """Create a new User instance with auto-generated ID.

        Args:
            properties: User properties containing name, age, and email.

        Returns:
            A new User instance with auto-generated UUID.
        """
        user = cls(
            name=Name(properties["name"]),
            age=Age(properties["age"]),
            email=Email(properties["email"]),
        )

        user.add_domain_event(
            UserCreated.create(
                aggregate_id=user.id,
                name=properties["name"],
                email=properties["email"],
                age=properties["age"],
            )
        )

        return user

    @classmethod
    def restore(cls, user_id: UUID, properties: UserProperties) -> "User":
        """Restore a User instance with existing ID.

        Args:
            user_id: The existing user ID.
            properties: User properties containing name, age, and email.

        Returns:
            A User instance with the specified ID.
        """
        user = cls(
            name=Name(properties["name"]),
            age=Age(properties["age"]),
            email=Email(properties["email"]),
        )
        user.id = user_id
        return user

    def is_adult(self) -> bool:
        """Check if the user is an adult.

        Query that returns whether the user is 18 years old or older.

        Returns:
            True if the user is 18 years old or older, False otherwise.
        """
        return self.age.is_adult()

    def change_email(self, new_email: str) -> None:
        """Change the user's email.

        Command that modifies the current instance's email.

        Args:
            new_email: The new email for the user.
        """
        old_email = self.email.value
        new_email_vo = Email(new_email)
        self.email = new_email_vo

        self.add_domain_event(
            UserEmailChanged.create(
                aggregate_id=self.id, old_email=old_email, new_email=new_email
            )
        )
