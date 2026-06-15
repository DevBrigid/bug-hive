import uuid


class User:
    """
    Represents a user of the BugHive system.

    A User can be an 'admin' or a 'developer'.
    Each user keeps a list of project IDs they are assigned to
    (one-to-many relationship: one user -> many projects).
    """

    VALID_ROLES = ("admin", "developer")

    def __init__(self, name, role="developer"):
        if role not in User.VALID_ROLES:
            raise ValueError(f"Role must be one of {User.VALID_ROLES}, got '{role}'")

        self.id = str(uuid.uuid4())[:8]   # short unique ID
        self.name = name
        self.role = role
        self.projects = []                # list of project IDs (one-to-many)

    def assign_project(self, project_id):
        #Link a project ID to this user (does nothing if already linked).
        if project_id not in self.projects:
            self.projects.append(project_id)

    def remove_project(self, project_id):
        # Unlink a project ID from this user.
        if project_id in self.projects:
            self.projects.remove(project_id)

    def to_dict(self):
        # Convert this User object into a JSON-serialisable dictionary.
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "projects": self.projects,
        }

    @classmethod
    def from_dict(cls, data):
        # Rebuild a User object from a dictionary (e.g. loaded from JSON).
        user = cls(data["name"], data["role"])
        user.id = data["id"]
        user.projects = data["projects"]
        return user

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', role='{self.role}')"