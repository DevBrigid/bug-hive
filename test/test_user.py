import pytest
from models.User import User


def test_user_creation_defaults():
    user = User("Alice")
    assert user.name == "Alice"
    assert user.role == "developer"        # default role
    assert user.projects == []
    assert isinstance(user.id, str)
    assert len(user.id) == 8                # short uuid


def test_user_creation_with_role():
    user = User("Bob", role="admin")
    assert user.role == "admin"


def test_user_invalid_role_raises():
    with pytest.raises(ValueError):
        User("Eve", role="superadmin")      # not a valid role


def test_assign_project():
    user = User("Alice")
    user.assign_project("proj123")
    assert "proj123" in user.projects

    # assigning the same project twice should not duplicate it
    user.assign_project("proj123")
    assert user.projects.count("proj123") == 1


def test_remove_project():
    user = User("Alice")
    user.assign_project("proj123")
    user.remove_project("proj123")
    assert "proj123" not in user.projects

    # removing something not present should not raise an error
    user.remove_project("does_not_exist")


def test_to_dict_and_from_dict_roundtrip():
    user = User("Carol", role="admin")
    user.assign_project("proj1")
    user.assign_project("proj2")

    data = user.to_dict()
    assert data["name"] == "Carol"
    assert data["role"] == "admin"
    assert data["projects"] == ["proj1", "proj2"]

    rebuilt = User.from_dict(data)
    assert rebuilt.id == user.id
    assert rebuilt.name == user.name
    assert rebuilt.role == user.role
    assert rebuilt.projects == user.projects


def test_repr_contains_key_info():
    user = User("Dan", role="developer")
    text = repr(user)
    assert "Dan" in text
    assert "developer" in text
    assert user.id in text