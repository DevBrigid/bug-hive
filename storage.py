import json
import os

from models.User import User
from models.project import Project
from models.bug import Bug


DB_PATH = os.path.join(os.path.dirname(__file__), "data", "db.json")


class Storage:
    """
    Holds all Users, Projects, and Bugs in memory while the app runs,
    and handles saving/loading everything to/from a local JSON file.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.users = []
        self.projects = []
        self.bugs = []

    # ------------------------------------------------------------------
    # USERS
    # ------------------------------------------------------------------

    def add_user(self, user: User):
        self.users.append(user)

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_name(self, name):
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None

    # ------------------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------------------

    def add_project(self, project: Project):
        self.projects.append(project)

    def get_project_by_id(self, project_id):
        for project in self.projects:
            if project.id == project_id:
                return project
        return None

    def get_project_by_name(self, name):
        for project in self.projects:
            if project.name.lower() == name.lower():
                return project
        return None

    def get_projects_by_user(self, user_id):
        return [p for p in self.projects if p.owner_id == user_id]

    # ------------------------------------------------------------------
    # BUGS
    # ------------------------------------------------------------------

    def add_bug(self, bug: Bug):
        self.bugs.append(bug)

    def get_bug_by_id(self, bug_id):
        for bug in self.bugs:
            if bug.id == bug_id:
                return bug
        return None

    def get_bugs_by_project(self, project_id):
        return [b for b in self.bugs if b.project_id == project_id]

    def get_bugs_by_assignee(self, user_id):
        return [b for b in self.bugs if user_id in b.assignees]

    def search_bugs(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.bugs if keyword in b.title.lower()]

    def filter_bugs(self, status=None, severity=None):
        results = self.bugs
        if status:
            results = [b for b in results if b.status == status]
        if severity:
            results = [b for b in results if b.severity == severity]
        return results

    # ------------------------------------------------------------------
    # PERSISTENCE
    # ------------------------------------------------------------------

    def save(self):
        """Write all current data to the JSON file."""
        data = {
            "users": [u.to_dict() for u in self.users],
            "projects": [p.to_dict() for p in self.projects],
            "bugs": [b.to_dict() for b in self.bugs],
        }

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        """Read all data from the JSON file, if it exists."""
        if not os.path.exists(self.db_path):
            return

        with open(self.db_path, "r") as f:
            data = json.load(f)

        self.users = [User.from_dict(u) for u in data.get("users", [])]
        self.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        self.bugs = [Bug.from_dict(b) for b in data.get("bugs", [])]