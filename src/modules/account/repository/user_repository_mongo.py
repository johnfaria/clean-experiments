"""MongoDB implementation of the User Repository."""

from bson import ObjectId
from src.modules.account.domain.user import User, UserProperties
from src.modules.account.repository.user_repository import AbstractUserRepository
from src.modules.core.infra.documents.user_document import UserDocument
from typing import override
from beanie import PydanticObjectId


class FailedToCreateUser(Exception):
    """Exception raised when user creation fails."""

    pass


class MongoUserRepository(AbstractUserRepository):
    """MongoDB implementation of the User Repository."""

    def __init__(self) -> None:
        """Initialize the MongoUserRepository."""
        self.document_model: type[UserDocument] = UserDocument

    @override
    async def get_user_by_id(self, user_id: str):
        """Get a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        user_document = await self.document_model.find_one(
            UserDocument.id == ObjectId(user_id)
        )
        if not user_document:
            return None
        properties = UserProperties(
            name=user_document.name, age=user_document.age, email=user_document.email
        )
        return User.restore(user_id=ObjectId(user_document.id), properties=properties)

    @override
    async def create_user(self, user_data: User) -> User:
        """Create a new user.

        Args:
            user_data: The User object to create.

        Returns:
            The created User object.

        Raises:
            FailedToCreateUser: If user creation fails.
        """
        user_document = self.document_model(
            id=PydanticObjectId(str(user_data.id)),
            name=user_data.name.value,
            age=user_data.age.value,
            email=user_data.email.value,
        )
        persisted_user = await self.document_model.insert_one(user_document)
        if not persisted_user:
            raise FailedToCreateUser("Failed to create user")
        return user_data

    @override
    async def update_user(self, user_id: str, user_data: User) -> User | None:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update.
            user_data: The User object with updated data.

        Returns:
            The updated User object if successful, otherwise None.
        """
        user_document = await self.document_model.find_one(
            UserDocument.id == ObjectId(user_id)
        )
        if not user_document:
            return None

        user_document.name = user_data.name.value
        user_document.age = user_data.age.value
        user_document.email = user_data.email.value

        await user_document.save()  # type: ignore
        return user_data

    @override
    async def delete_user(self, user_id: str) -> None:
        """Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            The deleted User object if successful, otherwise None.
        """
        user_document = await self.document_model.find_one(
            UserDocument.id == ObjectId(user_id)
        )
        if not user_document:
            return None
        await user_document.delete()  # type: ignore
        return None
