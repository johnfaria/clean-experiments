"""Use case for creating a new user."""

from dataclasses import dataclass

from src.modules.account.repository.user_repository import (
    AbstractUserRepository,
)
from src.modules.account.domain.user import User, UserProperties
from src.modules.core.domain.event_dispatcher import EventDispatcher


@dataclass
class CreateUserCommand:
    """Command to create a new user."""

    name: str
    age: int
    email: str


@dataclass(frozen=True)
class CreateUserUseCase:
    """Use case for creating a new user."""

    user_repository: AbstractUserRepository
    event_dispatcher: EventDispatcher

    async def execute(self, command: CreateUserCommand) -> User:
        """Execute the use case to create a user.

        Args:
            command: Command to create a new user.

        Returns:
            User: The newly created user entity.
        """
        user_properties = UserProperties(
            name=command.name, age=command.age, email=command.email
        )
        user = User.create(user_properties)
        _ = await self.user_repository.create_user(user)
        # Dispatch domain events after successful persistence
        self.event_dispatcher.dispatch(user.domain_events)
        user.clear_domain_events()
        return user
