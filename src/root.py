"""Composition root module for user management.

This module serves as the composition root for the application, demonstrating
the creation and usage of User entities with domain-specific functionality.
"""

from typing import cast

from beanie import init_beanie
from litestar import Litestar, Router
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.account.controllers.account_controllers import UserController
from src.modules.core.infra.documents.user_document import UserDocument
from src.settings import CONFIG


async def on_startup() -> None:
    """Initialize database connections and document models on application startup."""
    client: AsyncIOMotorClient = AsyncIOMotorClient(CONFIG.MONGO_URI)
    database: AsyncDatabase = cast(AsyncDatabase, client[CONFIG.MONGO_DATABASE])
    await init_beanie(database=database, document_models=[UserDocument])


def create_app() -> Litestar:
    """Create and configure the Litestar application.

    Returns:
        Litestar: The configured Litestar application instance.
    """
    router = Router(path="/api", route_handlers=[UserController])
    app = Litestar(route_handlers=[router], on_startup=[on_startup])
    return app
