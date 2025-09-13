"""Composition root module for user management.

This module serves as the composition root for the application, demonstrating
the creation and usage of User entities with domain-specific functionality.
"""

from litestar import Litestar, Router
from src.modules.account.controllers.account_controllers import UserController


def create_app() -> Litestar:
    """Create and configure the Litestar application.

    Returns:
        Litestar: The configured Litestar application instance.
    """
    router = Router(path="/api", route_handlers=[UserController])
    app = Litestar(route_handlers=[router])
    return app
