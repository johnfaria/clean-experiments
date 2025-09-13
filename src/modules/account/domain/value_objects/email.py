"""Email value object module.

This module defines the Email value object with validation logic
for user email addresses in the domain.
"""

import re
from dataclasses import dataclass
from typing import override


@dataclass(frozen=True)
class Email:
    """Represents a valid email address.

    A value object that encapsulates email validation logic
    and ensures email integrity in the domain.

    Attributes:
        value: The email string value.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate email after initialization.

        Raises:
            ValueError: If the email is empty, exceeds 254 characters, or does not match the required format.
        """
        if not self.value:
            raise ValueError("Email cannot be empty")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, self.value):
            raise ValueError("Invalid email format")

        if len(self.value) > 254:
            raise ValueError("Email cannot exceed 254 characters")

    @property
    def domain(self) -> str:
        """Get the domain part of the email.

        Returns:
            The domain part of the email address.
        """
        return self.value.split("@")[1]

    @property
    def local_part(self) -> str:
        """Get the local part of the email.

        Returns:
            The local part of the email address (before @).
        """
        return self.value.split("@")[0]

    @override
    def __str__(self) -> str:
        """Return the string representation of the email."""
        return self.value
