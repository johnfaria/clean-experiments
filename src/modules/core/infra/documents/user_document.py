"""User Document model using Beanie ODM."""

from beanie import Document


class UserDocument(Document):
    """Beanie Document model for User."""

    name: str
    age: int
    email: str
