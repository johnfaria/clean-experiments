"""Age value object module.

This module defines the Age value object with validation logic
for user ages in the domain.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Age:
    """Represents a valid user age.

    A value object that encapsulates age validation logic
    and ensures age integrity in the domain.

    Attributes:
        value: The age integer value.
    """

    value: int

    def __post_init__(self) -> None:
        """Validate age after initialization.

        Raises:
            ValueError: If age is negative or exceeds 150 years.
        """
        if self.value < 0:
            raise ValueError("Age cannot be negative")

        if self.value > 150:
            raise ValueError("Age cannot exceed 150 years")

    def is_adult(self) -> bool:
        """Check if the age represents an adult.

        Returns:
            True if age is 18 or older, False otherwise.
        """
        return self.value >= 18

    def __str__(self) -> str:
        """Return the string representation of the age."""
        return str(self.value)
