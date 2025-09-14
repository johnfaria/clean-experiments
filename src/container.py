"""Dependency injection container setup."""

from lagom import Container

from src.modules.account.config.event_config import create_configured_event_dispatcher
from src.modules.account.repository.user_repository_mongo import (
    MongoUserRepository,
)
from src.modules.account.use_case.create_user_use_case import CreateUserUseCase
from src.modules.account.use_case.delete_user_use_case import DeleteUserUseCase
from src.modules.account.use_case.get_user_use_case import GetUserUseCase
from src.modules.account.use_case.update_user_use_case import UpdateUserUseCase
from src.modules.core.domain.event_dispatcher import EventDispatcher
from src.settings import CONFIG, Settings

container = Container()

container[Settings] = CONFIG

# Register repository implementation
container[MongoUserRepository] = MongoUserRepository()

# Register pre-configured event dispatcher
container[EventDispatcher] = create_configured_event_dispatcher()

# Register use cases
container[CreateUserUseCase] = lambda c: CreateUserUseCase(
    user_repository=c[MongoUserRepository], event_dispatcher=c[EventDispatcher]
)
container[GetUserUseCase] = lambda c: GetUserUseCase(
    user_repository=c[MongoUserRepository],
)
container[UpdateUserUseCase] = lambda c: UpdateUserUseCase(
    user_repository=c[MongoUserRepository], event_dispatcher=c[EventDispatcher]
)

container[DeleteUserUseCase] = lambda c: DeleteUserUseCase(
    user_repository=c[MongoUserRepository], event_dispatcher=c[EventDispatcher]
)
