from models.User import User

def test_user_initialization():
    u = User("Alice", "admin")
    assert u.username == "Alice"
    assert u.role == "admin"

def test_user_serialization():
    u = User("Bob", "developer")
    d = u.to_dict()
    assert d["username"] == "Bob"
    assert d["role"] == "developer"