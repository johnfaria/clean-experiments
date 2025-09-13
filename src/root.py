"""Composition root module for user management.

This module serves as the composition root for the application, demonstrating
the creation and usage of User entities with domain-specific functionality.
"""

from litestar import Litestar, Router
from src.modules.account.controllers.account_controllers import UserController
from src.settings import CONFIG
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.modules.core.infra.documents.user_document import UserDocument


async def on_startup() -> None:
    """On startup event handler to initialize database connection and Beanie."""
    client = AsyncIOMotorClient(CONFIG.MONGO_URI)
    await init_beanie(database=client.dev, document_models=[UserDocument])


def create_app() -> Litestar:
    """Create and configure the Litestar application.

    Returns:
        Litestar: The configured Litestar application instance.
    """
    router = Router(path="/api", route_handlers=[UserController])
    app = Litestar(route_handlers=[router], on_startup=[on_startup])
    return app
