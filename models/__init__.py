"""
models package — contains the core data classes for BugHive:
User, Project, and Bug.
"""

from .User import User
from .Project import Project
from .Bug import Bug
from .Gamification import Gamification

__all__ = ["User", "Project", "Bug", "Gamification"]