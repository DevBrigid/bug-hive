class Project:
    def __init__(self, name, description, members=None):
        self.name = name
        self.description = description
        self.members = members if members is not None else []

    def assign_user(self, username):
        """Encapsulated business rule: prevent duplicate member assignment"""
        if username not in self.members:
            self.members.append(username)
            return True
        return False

    def to_dict(self):
        return {"name": self.name, "description": self.description, "members": self.members}

    @staticmethod
    def from_dict(data):
        return Project(data["name"], data["description"], data.get("members", []))