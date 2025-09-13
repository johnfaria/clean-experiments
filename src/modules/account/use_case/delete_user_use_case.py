"""Use case for deleting a user by ID."""

from dataclasses import dataclass

from src.modules.account.repository.user_repository import AbstractUserRepository
from src.modules.account.use_case.update_user_use_case import UserNotFoundException
from src.modules.core.domain.event_dispatcher import EventDispatcher


@dataclass
class DeleteUserCommand:
    """Command to delete a user by ID."""

    user_id: str


@dataclass(frozen=True)
class DeleteUserUseCase:
    """Use case for deleting a user by ID."""

    user_repository: AbstractUserRepository
    event_dispatcher: EventDispatcher

    async def execute(self, command: DeleteUserCommand) -> None:
        """Execute the use case to delete a user.

        Args:
            command: Command containing the user ID to delete.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        existing_user = await self.user_repository.get_user_by_id(command.user_id)
        if not existing_user:
            raise UserNotFoundException(f"User with ID {command.user_id} not found")

        await self.user_repository.delete_user(command.user_id)
        # Dispatch domain events after successful deletion
        self.event_dispatcher.dispatch(existing_user.domain_events)
        existing_user.clear_domain_events()
