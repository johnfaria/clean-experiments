"""User repository interface."""

from abc import ABC, abstractmethod
from typing import override

from src.modules.account.domain.user import User


class AbstractUserRepository(ABC):
    """Abstract methods for user repository operations."""

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None:
        """Get a user by their ID."""
        pass

    @abstractmethod
    async def create_user(self, user_data: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    def update_user(self, user_id: str, user_data: User) -> User | None:
        """Update an existing user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> User | None:
        """Delete a user by their ID."""
        pass


class InMemoryUserRepository(AbstractUserRepository):
    """In-memory implementation of the user repository."""

    def __init__(self):
        """Initialize the in-memory user repository."""
        self.users: dict[str, User] = {}

    @override
    def get_user_by_id(self, user_id: str) -> User | None:
        """Get a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        return self.users.get(user_id)

    @override
    async def create_user(self, user_data: User) -> User:
        """Create a new user.

        Args:
            user_data: The User object to create.

        Returns:
            The created User object.
        """
        self.users[str(user_data.id)] = user_data
        return user_data

    @override
    def update_user(self, user_id: str, user_data: User) -> User | None:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update.
            user_data: The updated User object.

        Returns:
            The updated User object if the user exists, otherwise None.
        """
        if user_id in self.users:
            self.users[user_id] = user_data
            return user_data
        return None

    @override
    def delete_user(self, user_id: str) -> User | None:
        """Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            The deleted User object if the user existed, otherwise None.
        """
        return self.users.pop(user_id, None)
