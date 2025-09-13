"""Event configuration module.

This module provides a more advanced approach to event handler
registration using a configuration class pattern.
"""

from src.modules.core.domain.event_dispatcher import EventDispatcher
from src.modules.account.handlers.user_handlers import (
    UserNotificationHandler,
    UserAuditHandler,
    UserAnalyticsHandler,
)
from src.modules.account.domain.events import UserCreated, UserEmailChanged


class EventConfiguration:
    """Centralized event configuration.

    This class provides a structured way to configure all
    event handlers and their subscriptions.
    """

    @staticmethod
    def configure_dispatcher(dispatcher: EventDispatcher) -> None:
        """Configure the event dispatcher with all handlers.

        Args:
            dispatcher: The event dispatcher to configure.
        """
        # User event handlers
        EventConfiguration._configure_user_events(dispatcher)

        # Future: Other domain event configurations can be added here
        # EventConfiguration._configure_order_events(dispatcher)
        # EventConfiguration._configure_payment_events(dispatcher)

    @staticmethod
    def _configure_user_events(dispatcher: EventDispatcher) -> None:
        """Configure handlers for user domain events.

        Args:
            dispatcher: The event dispatcher to configure.
        """
        # Create handler instances
        notification_handler = UserNotificationHandler()
        audit_handler = UserAuditHandler()
        analytics_handler = UserAnalyticsHandler()

        # UserCreated event subscriptions
        dispatcher.subscribe(UserCreated, notification_handler)
        dispatcher.subscribe(UserCreated, audit_handler)
        dispatcher.subscribe(UserCreated, analytics_handler)

        # UserEmailChanged event subscriptions
        dispatcher.subscribe(UserEmailChanged, notification_handler)
        dispatcher.subscribe(UserEmailChanged, audit_handler)
        dispatcher.subscribe(UserEmailChanged, analytics_handler)


def create_configured_event_dispatcher() -> EventDispatcher:
    """Create and configure an event dispatcher.

    Factory function that creates an EventDispatcher instance
    and configures it with all necessary handlers.

    Returns:
        A fully configured EventDispatcher instance.
    """
    dispatcher = EventDispatcher()
    EventConfiguration.configure_dispatcher(dispatcher)
    return dispatcher
