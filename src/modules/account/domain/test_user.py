"""Unit tests for the User entity in the account domain."""

from uuid import UUID

import pytest

from src.modules.account.domain.user import User


class TestUser:
    """Unit tests for the User entity."""

    def test_user_creation(self):
        """Test that a User can be created with valid attributes."""
        user = User(name="John Doe", age=25, email="john@example.com")

        assert user.name == "John Doe"
        assert user.age == 25
        assert user.email == "john@example.com"
        assert isinstance(user.id, UUID)

    def test_user_inherits_from_entity(self):
        """Test that User inherits Entity properties."""
        user = User(name="Jane Doe", age=30, email="jane@example.com")

        # Should have auto-generated UUID
        assert hasattr(user, "id")
        assert isinstance(user.id, UUID)

    def test_is_adult_returns_true_for_18_and_older(self):
        """Test is_adult returns True for users 18 and older."""
        adult_user = User(name="Adult User", age=18, email="adult@example.com")
        older_user = User(name="Older User", age=25, email="older@example.com")

        assert adult_user.is_adult() is True
        assert older_user.is_adult() is True

    def test_is_adult_returns_false_for_under_18(self):
        """Test is_adult returns False for users under 18."""
        minor_user = User(name="Minor User", age=17, email="minor@example.com")
        child_user = User(name="Child User", age=10, email="child@example.com")

        assert minor_user.is_adult() is False
        assert child_user.is_adult() is False

    def test_user_equality_based_on_id(self):
        """Test that User equality is based on ID (inherited from Entity)."""
        user1 = User(name="John Doe", age=25, email="john@example.com")
        user2 = User(name="Jane Doe", age=30, email="jane@example.com")

        # Different users should not be equal
        assert user1 != user2

        # Same user instance should be equal to itself
        assert user1 == user1

    def test_user_hash_based_on_id(self):
        """Test that User hash is based on ID (inherited from Entity)."""
        user1 = User(name="John Doe", age=25, email="john@example.com")
        user2 = User(name="Jane Doe", age=30, email="jane@example.com")

        # Different users should have different hashes
        assert hash(user1) != hash(user2)

        # Same user should have consistent hash
        assert hash(user1) == hash(user1)

    def test_users_can_be_used_in_sets(self):
        """Test that Users can be used in sets (due to hash implementation)."""
        user1 = User(name="John Doe", age=25, email="john@example.com")
        user2 = User(name="Jane Doe", age=30, email="jane@example.com")

        user_set = {user1, user2}
        assert len(user_set) == 2

        # Adding same user again should not increase set size
        user_set.add(user1)
        assert len(user_set) == 2

    @pytest.mark.parametrize(
        "age,expected",
        [(0, False), (17, False), (18, True), (25, True), (65, True), (100, True)],
    )
    def test_is_adult_edge_cases(self, age: int, expected: bool):
        """Test is_adult method with various age values."""
        user = User(name="Test User", age=age, email="test@example.com")
        assert user.is_adult() == expected

    def test_user_with_empty_string_values(self):
        """Test User creation with edge case string values."""
        user = User(name="", age=25, email="")

        assert user.name == ""
        assert user.email == ""
        assert user.age == 25
        assert user.is_adult() is True

    def test_user_dataclass_representation(self):
        """Test that User has proper string representation from dataclass."""
        user = User(name="John Doe", age=25, email="john@example.com")

        repr_str = repr(user)
        assert "User(" in repr_str
        assert "name='John Doe'" in repr_str
        assert "age=25" in repr_str
        assert "email='john@example.com'" in repr_str
