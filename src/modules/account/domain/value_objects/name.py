"""Name value object module.

This module defines the Name value object with validation logic
for user names in the domain.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    """Represents a valid user name.

    A value object that encapsulates name validation logic
    and ensures name integrity in the domain.

    Attributes:
        value: The name string value.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate name after initialization.

        Raises:
            ValueError: If the name is empty, has fewer than 2 characters, or exceeds 100 characters.
        """
        if not self.value or self.value.strip() == "":
            raise ValueError("Name cannot be empty")

        if len(self.value.strip()) < 2:
            raise ValueError("Name must have at least 2 characters")

        if len(self.value) > 100:
            raise ValueError("Name cannot exceed 100 characters")

    def __str__(self) -> str:
        """Return the string representation of the name."""
        return self.value
