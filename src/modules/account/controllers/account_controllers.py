"""Account Controllers Module."""

from typing import Annotated, final
from litestar import Controller, post, get, put, delete

from dataclasses import dataclass
from litestar.dto import DataclassDTO
from litestar.params import Body

from src.modules.account.use_case.create_user_use_case import (
    CreateUserCommand,
    CreateUserUseCase,
)
from src.modules.account.use_case.delete_user_use_case import (
    DeleteUserCommand,
    DeleteUserUseCase,
)
from src.modules.account.use_case.get_user_use_case import (
    GetUserQuery,
    GetUserUseCase,
)
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from src.container import container
from src.modules.account.use_case.update_user_use_case import (
    UpdateUserCommand,
    UpdateUserUseCase,
)


@dataclass
class UserWrite:
    """User data for creation.

    This represents the input data required to create a new user in the system.
    All fields are mandatory and will be validated according to business rules.
    """

    name: str
    age: int
    email: str


UserWriteDTO = DataclassDTO[UserWrite]


@dataclass
class UserRead:
    """User data representation.

    This represents a complete user record as stored in the system,
    including the unique identifier generated upon creation.
    """

    user_id: str
    name: str
    age: int
    email: str


UserReadDTO = DataclassDTO[UserRead]


@dataclass
class UserUpdate:
    """User data for update.

    This represents the input data required to update an existing user in the system.
    All fields are optional and will be validated according to business rules.
    """

    name: str | None = None
    age: int | None = None
    email: str | None = None


UserUpdateDTO = DataclassDTO[UserUpdate]


@final
class UserController(Controller):
    """Controller for user-related operations.

    This controller handles all user management operations including:
    - User creation with validation and business rule enforcement
    - User data retrieval and management
    - User profile updates (future implementation)
    - User deletion (future implementation)

    All endpoints follow RESTful conventions and provide comprehensive
    error handling with detailed feedback for different failure scenarios.

    **Security:** All endpoints require proper authentication and authorization.
    **Rate Limiting:** Create operations are limited to prevent abuse.
    **Validation:** All input data is validated according to business rules.
    """

    path = "/users"
    tags = ["Users"]

    @post(
        dto=UserWriteDTO,
        return_dto=UserReadDTO,
        status_code=201,
        summary="Create New User",
        description="""
        Creates a new user in the system with the provided information.
        
        This endpoint validates the input data, applies business rules, and creates
        a new user record. The user will be assigned a unique identifier and the
        complete user information will be returned.
        
        **Business Rules:**
        - Name must be between 2 and 100 characters
        - Age must be between 18 and 120 years
        - Email must be unique and in valid format
        - All fields are required
        """,
        response_description="Successfully created user with generated ID",
        operation_id="create_user",
        dependencies={
            "create_user_use_case": Provide(
                lambda: container[CreateUserUseCase], sync_to_thread=False
            ),
        },
    )
    async def create_user(
        self,
        data: Annotated[
            UserWrite,
            Body(
                title="User Creation Data",
                description="Complete user information required for account creation. All fields are mandatory and subject to validation.",
            ),
        ],
        create_user_use_case: CreateUserUseCase,
    ) -> UserRead:
        """Create a new user in the system.

        This endpoint creates a new user account with the provided information.
        All input data is validated according to business rules before creating
        the user record.

        Args:
            data: User creation data containing name, age, and email
            create_user_use_case: Injected use case for user creation business logic

        Returns:
            UserRead: Complete user information including the generated unique ID
        """
        command = CreateUserCommand(name=data.name, age=data.age, email=data.email)
        domain_user = await create_user_use_case.execute(command)
        return UserRead(
            name=domain_user.name.value,
            age=domain_user.age.value,
            email=domain_user.email.value,
            user_id=str(domain_user.id),
        )

    @get(
        "/{user_id:str}",
        dto=UserUpdateDTO,
        return_dto=UserReadDTO,
        summary="Get User by ID",
        description="""
        Retrieves a user by their unique identifier.
        
        This endpoint returns the complete user information for the specified user ID.
        If the user is not found, a 404 error will be returned.
        
        **Authorization:** Requires valid authentication token.
        **Rate Limiting:** Standard rate limits apply.
        """,
        response_description="Successfully retrieved user information",
        operation_id="get_user",
        dependencies={
            "get_user_use_case": Provide(
                lambda: container[GetUserUseCase], sync_to_thread=False
            ),
        },
    )
    async def get_user(
        self,
        user_id: str,
        get_user_use_case: GetUserUseCase,
    ) -> UserRead:
        """Retrieve a user by their ID.

        This endpoint retrieves a user from the repository using their unique identifier.
        If the user is not found, a 404 Not Found exception is raised.

        Args:
            user_id: The unique identifier of the user to retrieve
            get_user_use_case: Injected use case for user retrieval business logic

        Returns:
            UserRead: Complete user information for the requested user
        """
        query = GetUserQuery(user_id=user_id)
        domain_user = await get_user_use_case.execute(query)

        return UserRead(
            name=domain_user.name.value,
            age=domain_user.age.value,
            email=domain_user.email.value,
            user_id=str(domain_user.id),
        )

    @put(
        "/{user_id:str}",
        summary="Update User by ID",
        description="""
        Updates user information for the specified user ID.

        This endpoint allows modification of user details such as name, age, and email.
        All fields are optional; only provided fields will be updated. Input data is validated
        according to business rules before applying changes.

        **Business Rules:**
        - Name, if provided, must be between 2 and 100 characters
        - Age, if provided, must be between 18 and 120 years
        - Email, if provided, must be unique and in valid format

        **Authorization:** Requires valid authentication token.
        **Rate Limiting:** Standard rate limits apply.
        **Error Handling:** Returns 404 if user is not found, 400 for validation errors.
        """,
        operation_id="update_user",
        dependencies={
            "update_user_use_case": Provide(
                lambda: container[UpdateUserUseCase], sync_to_thread=False
            ),
        },
    )
    async def update_user(
        self, user_id: str, data: UserUpdate, update_user_use_case: UpdateUserUseCase
    ) -> UserRead:
        """Update user information by ID.

        This endpoint is a placeholder for future implementation of user updates.
        It will allow modification of user details such as name, age, and email.

        Args:
            user_id: The unique identifier of the user to update
            data: The updated user information
            update_user_use_case: Injected use case for user update business logic

        Returns:
            UserRead: Complete updated user information

        """
        command = UpdateUserCommand(
            user_id=user_id, name=data.name, age=data.age, email=data.email
        )
        updated_user = await update_user_use_case.execute(command)
        return UserRead(
            name=updated_user.name.value,
            age=updated_user.age.value,
            email=updated_user.email.value,
            user_id=str(updated_user.id),
        )

    @delete(
        "/{user_id:str}",
        summary="Delete User by ID",
        description="""
        Deletes a user by their unique identifier.

        This endpoint removes the user record from the system if it exists.
        If the user is not found, a 404 error will be returned.

        **Authorization:** Requires valid authentication token.
        **Rate Limiting:** Standard rate limits apply.
        **Error Handling:** Returns 404 if user is not found.
        """,
        operation_id="delete_user",
        dependencies={
            "delete_user_use_case": Provide(
                lambda: container[DeleteUserUseCase], sync_to_thread=False
            ),
        },
    )
    async def delete_user(
        self, user_id: str, delete_user_use_case: DeleteUserUseCase
    ) -> None:
        """Delete a user by their ID.

        This endpoint is a placeholder for future implementation of user deletion.
        It will remove the user record from the system.

        Args:
            user_id: The unique identifier of the user to delete
            delete_user_use_case: Injected use case for user deletion business logic

        Returns:
            None
        """
        command = DeleteUserCommand(user_id=user_id)
        await delete_user_use_case.execute(command)
        return None
