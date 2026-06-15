import datetime

class Bug:
    def __init__(self, bug_id, title, project_name, severity, assignees=None, status="open", created_at=None, resolved_at=None):
        self.bug_id = int(bug_id)
        self.title = title
        self.project_name = project_name
        self.severity = severity.lower()  # low, medium, high
        self.assignees = assignees if assignees is not None else []
        self.status = status  # open, resolved
        self.created_at = created_at or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.resolved_at = resolved_at

    def resolve(self):
        if self.status == "open":
            self.status = "resolved"
            self.resolved_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            return True
        return False

    def to_dict(self):
        return {
            "bug_id": self.bug_id,
            "title": self.title,
            "project_name": self.project_name,
            "severity": self.severity,
            "assignees": self.assignees,
            "status": self.status,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at
        }

    @staticmethod
    def from_dict(data):
        return Bug(
            data["bug_id"], data["title"], data["project_name"], data["severity"],
            data.get("assignees", []), data["status"], data["created_at"], data["resolved_at"]
        )