"""User event handlers module.

This module contains handlers for user domain events,
implementing specific business logic that should occur
when user events are raised.
"""

from typing import override

from src.modules.account.domain.events import UserCreated, UserEmailChanged
from src.modules.core.domain.domain_event import DomainEvent
from src.modules.core.domain.event_dispatcher import EventHandler


class UserNotificationHandler(EventHandler):
    """Handler for sending notifications when user events occur.

    This handler is responsible for sending notifications
    (email, SMS, push notifications, etc.) when important
    user events happen.
    """

    @override
    def handle(self, event: DomainEvent) -> None:
        """Handle user events and send appropriate notifications.

        Args:
            event: The user domain event to handle.
        """
        if isinstance(event, UserCreated):
            self._handle_user_created(event)
        elif isinstance(event, UserEmailChanged):
            self._handle_user_email_changed(event)

    def _handle_user_created(self, event: UserCreated) -> None:
        """Handle UserCreated event."""
        print(f"📧 Sending welcome email to {event.email}")
        print(f"📱 Sending welcome SMS to user {event.name}")
        # Here you would integrate with email/SMS services

    def _handle_user_email_changed(self, event: UserEmailChanged) -> None:
        """Handle UserEmailChanged event."""
        print(f"📧 Sending email change confirmation to {event.new_email}")
        print(f"📧 Sending notification to old email {event.old_email}")
        # Here you would integrate with email services


class UserAuditHandler(EventHandler):
    """Handler for auditing user events.

    This handler is responsible for logging user events
    for audit trails, compliance, and analytics purposes.
    """

    @override
    def handle(self, event: DomainEvent) -> None:
        """Handle user events and create audit logs.

        Args:
            event: The user domain event to handle.
        """
        if isinstance(event, UserCreated):
            self._handle_user_created(event)
        elif isinstance(event, UserEmailChanged):
            self._handle_user_email_changed(event)

    def _handle_user_created(self, event: UserCreated) -> None:
        """Handle UserCreated event for audit."""
        print(
            f"📊 AUDIT: User created - ID: {event.aggregate_id}, Email: {event.email}"
        )
        # Here you would log to audit database/service

    def _handle_user_email_changed(self, event: UserEmailChanged) -> None:
        """Handle UserEmailChanged event for audit."""
        print(f"📊 AUDIT: User email changed - ID: {event.aggregate_id}")
        print(f"📊 AUDIT: Old: {event.old_email} → New: {event.new_email}")
        # Here you would log to audit database/service


class UserAnalyticsHandler(EventHandler):
    """Handler for user analytics and metrics.

    This handler is responsible for tracking user events
    for business intelligence and analytics purposes.
    """

    @override
    def handle(self, event: DomainEvent) -> None:
        """Handle user events and track analytics.

        Args:
            event: The user domain event to handle.
        """
        if isinstance(event, UserCreated):
            self._handle_user_created(event)
        elif isinstance(event, UserEmailChanged):
            self._handle_user_email_changed(event)

    def _handle_user_created(self, event: UserCreated) -> None:
        """Handle UserCreated event for analytics."""
        print(f"📈 ANALYTICS: New user registered - Age: {event.age}")
        # Here you would send to analytics service (e.g., Mixpanel, Google Analytics)

    def _handle_user_email_changed(self, _event: UserEmailChanged) -> None:
        """Handle UserEmailChanged event for analytics."""
        print(f"📈 ANALYTICS: User email change event")
        # Here you would track email change events
