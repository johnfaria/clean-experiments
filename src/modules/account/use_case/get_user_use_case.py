"""Use case for retrieving a user by ID."""

from dataclasses import dataclass

from src.modules.account.repository.user_repository import (
    AbstractUserRepository,
)
from src.modules.account.domain.user import User


@dataclass
class GetUserQuery:
    """Query to retrieve a user by ID."""

    user_id: str


@dataclass(frozen=True)
class GetUserUseCase:
    """Use case for retrieving a user by ID."""

    user_repository: AbstractUserRepository

    async def execute(self, query: GetUserQuery) -> User | None:
        """Execute the use case to retrieve a user.

        Args:
            query: The query containing the user ID to retrieve

        Returns:
            User if found, None otherwise
        """
        return await self.user_repository.get_user_by_id(query.user_id)
