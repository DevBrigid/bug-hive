import uuid
from datetime import date


class Bug:
    """
    Represents a bug/task in the BugHive system.
    A Bug belongs to one Project, but can have many assignees (developers)
    working on it (many-to-many relationship: bugs <-> users).
    """

    VALID_SEVERITIES = ("low", "medium", "high")
    VALID_STATUSES = ("open", "resolved")

    def __init__(self, title, description, severity, project_id):
        if severity not in Bug.VALID_SEVERITIES:
            raise ValueError(
                f"Severity must be one of {Bug.VALID_SEVERITIES}, got '{severity}'"
            )

        self.id = str(uuid.uuid4())[:8]     # short unique ID
        self.title = title
        self.description = description
        self.severity = severity
        self.status = "open"                # open or resolved
        self.project_id = project_id        # FK -> Project.id
        self.assignees = []                 # list of user IDs (many-to-many)
        self.created_at = str(date.today())
        self.resolved_at = None

    def assign(self, user_id):
        # Add a developer (user ID) to this bug's list of assignees.
        if user_id not in self.assignees:
            self.assignees.append(user_id)

    def unassign(self, user_id):
        # Remove a developer (user ID) from this bug's assignees.
        if user_id in self.assignees:
            self.assignees.remove(user_id)

    def resolve(self):
        # Mark this bug as resolved and record the resolution date.
        self.status = "resolved"
        self.resolved_at = str(date.today())

    def reopen(self):
        # Reopen a resolved bug — sets status back to open.
        self.status = "open"
        self.resolved_at = None

    def to_dict(self):
        # Convert this Bug object into a JSON-serialisable dictionary.
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "project_id": self.project_id,
            "assignees": self.assignees,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
        }

    @classmethod
    def from_dict(cls, data):
        # Rebuild a Bug object from a dictionary (e.g. loaded from JSON).
        bug = cls(data["title"], data["description"], data["severity"], data["project_id"])
        bug.id = data["id"]
        bug.status = data["status"]
        bug.assignees = data["assignees"]
        bug.created_at = data["created_at"]
        bug.resolved_at = data["resolved_at"]
        return bug

    def __repr__(self):
        return f"Bug(id={self.id}, title='{self.title}', status='{self.status}')"