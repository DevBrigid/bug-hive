class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role  # admin or developer

    def to_dict(self):
        return {"username": self.username, "role": self.role}

    @staticmethod
    def from_dict(data):
        return User(data["username"], data["role"])