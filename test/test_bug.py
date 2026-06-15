import pytest
from models.Bug import Bug


def test_bug_creation_defaults():
    bug = Bug("Navbar crash", "Crashes on mobile Safari", "high", project_id="proj123")
    assert bug.title == "Navbar crash"
    assert bug.description == "Crashes on mobile Safari"
    assert bug.severity == "high"
    assert bug.status == "open"             # all new bugs start open
    assert bug.project_id == "proj123"
    assert bug.assignees == []
    assert bug.resolved_at is None
    assert isinstance(bug.id, str)
    assert len(bug.id) == 8
    assert bug.created_at  # not empty


def test_invalid_severity_raises():
    with pytest.raises(ValueError):
        Bug("Bad bug", "desc", "critical", project_id="proj123")  # not a valid severity


def test_assign_and_unassign():
    bug = Bug("Login bug", "desc", "medium", project_id="proj123")

    bug.assign("user1")
    bug.assign("user2")
    assert bug.assignees == ["user1", "user2"]

    # assigning the same user twice should not duplicate it
    bug.assign("user1")
    assert bug.assignees.count("user1") == 1

    bug.unassign("user1")
    assert "user1" not in bug.assignees
    assert bug.assignees == ["user2"]

    # unassigning someone not present should not raise an error
    bug.unassign("does_not_exist")


def test_resolve_sets_status_and_date():
    bug = Bug("Footer overlap", "desc", "low", project_id="proj123")
    assert bug.status == "open"
    assert bug.resolved_at is None

    bug.resolve()

    assert bug.status == "resolved"
    assert bug.resolved_at is not None


def test_reopen_clears_resolution():
    bug = Bug("Footer overlap", "desc", "low", project_id="proj123")
    bug.resolve()
    assert bug.status == "resolved"

    bug.reopen()

    assert bug.status == "open"
    assert bug.resolved_at is None


def test_to_dict_and_from_dict_roundtrip():
    bug = Bug("Crash on save", "App crashes when saving", "high", project_id="proj123")
    bug.assign("user1")
    bug.resolve()

    data = bug.to_dict()
    assert data["title"] == "Crash on save"
    assert data["severity"] == "high"
    assert data["status"] == "resolved"
    assert data["assignees"] == ["user1"]
    assert data["resolved_at"] is not None

    rebuilt = Bug.from_dict(data)
    assert rebuilt.id == bug.id
    assert rebuilt.title == bug.title
    assert rebuilt.severity == bug.severity
    assert rebuilt.status == bug.status
    assert rebuilt.assignees == bug.assignees
    assert rebuilt.resolved_at == bug.resolved_at


def test_repr_contains_key_info():
    bug = Bug("Crash on save", "desc", "high", project_id="proj123")
    text = repr(bug)
    assert "Crash on save" in text
    assert "open" in text
    assert bug.id in text