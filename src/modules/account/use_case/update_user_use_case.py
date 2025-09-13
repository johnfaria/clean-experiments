"""Use case for updating an existing user."""

from dataclasses import dataclass

from src.modules.account.domain.events import UserEmailChanged
from src.modules.account.domain.user import User, UserProperties
from src.modules.account.repository.user_repository import AbstractUserRepository
from src.modules.core.domain.event_dispatcher import EventDispatcher


class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    pass


@dataclass
class UpdateUserCommand:
    """Command to update an existing user."""

    user_id: str
    name: str | None = None
    age: int | None = None
    email: str | None = None


@dataclass(frozen=True)
class UpdateUserUseCase:
    """Use case for updating an existing user."""

    user_repository: AbstractUserRepository
    event_dispatcher: EventDispatcher

    async def execute(self, command: UpdateUserCommand) -> User:
        """Execute the use case to update a user.

        Args:
            command: Command containing user ID and fields to update.

        Returns:
            User: The updated user entity.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        existing_user = await self.user_repository.get_user_by_id(command.user_id)
        if not existing_user:
            raise UserNotFoundException(f"User with ID {command.user_id} not found")

        updated_properties = UserProperties(
            name=command.name if command.name is not None else existing_user.name.value,
            age=command.age if command.age is not None else existing_user.age.value,
            email=command.email
            if command.email is not None
            else existing_user.email.value,
        )

        updated_user = User.restore(
            user_id=existing_user.id, properties=updated_properties
        )

        _ = await self.user_repository.update_user(
            user_id=command.user_id, user_data=updated_user
        )
        # Dispatch domain events after successful persistence
        self.event_dispatcher.dispatch(updated_user.domain_events)
        updated_user.clear_domain_events()
        return updated_user
