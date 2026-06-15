import uuid
from datetime import date


class Project:
    """
    Represents a project in the BugHive system.

    A Project belongs to one owner (User) but can have many bugs
    (one-to-many relationship: one project -> many bugs).
    """

    def __init__(self, name, owner_id):
        self.id = str(uuid.uuid4())[:8]    # short unique ID
        self.name = name
        self.owner_id = owner_id           # FK -> User.id
        self.bugs = []                     # list of bug IDs (one-to-many)
        self.created_at = str(date.today())

    def add_bug(self, bug_id):
        # Link a bug ID to this project (does nothing if already linked).
        if bug_id not in self.bugs:
            self.bugs.append(bug_id)

    def remove_bug(self, bug_id):
        # Unlink a bug ID from this project.
        if bug_id in self.bugs:
            self.bugs.remove(bug_id)

    def to_dict(self):
        # Convert this Project object into a JSON-serialisable dictionary.
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "bugs": self.bugs,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        # Rebuild a Project object from a dictionary (e.g. loaded from JSON).
        project = cls(data["name"], data["owner_id"])
        project.id = data["id"]
        project.bugs = data["bugs"]
        project.created_at = data["created_at"]
        return project

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}', owner_id={self.owner_id})"