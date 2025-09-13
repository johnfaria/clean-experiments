"""Dependency injection container setup."""

from lagom import Container

from src.modules.account.repository.user_repository import (
    InMemoryUserRepository,
)
from src.modules.account.use_case.create_user_use_case import CreateUserUseCase
from src.modules.account.use_case.get_user_use_case import GetUserUseCase
from src.modules.core.domain.event_dispatcher import EventDispatcher

from src.modules.account.config.event_config import create_configured_event_dispatcher

container = Container()

# Register repository implementation
container[InMemoryUserRepository] = InMemoryUserRepository()

# Register pre-configured event dispatcher
container[EventDispatcher] = create_configured_event_dispatcher()

# Register use cases
container[CreateUserUseCase] = lambda c: CreateUserUseCase(
    user_repository=c[InMemoryUserRepository], event_dispatcher=c[EventDispatcher]
)
container[GetUserUseCase] = lambda c: GetUserUseCase(
    user_repository=c[InMemoryUserRepository],
)
