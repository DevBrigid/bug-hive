from models.Project import Project


def test_project_creation():
    project = Project("Website Redesign", owner_id="user123")
    assert project.name == "Website Redesign"
    assert project.owner_id == "user123"
    assert project.bugs == []
    assert isinstance(project.id, str)
    assert len(project.id) == 8
    assert project.created_at  # not empty


def test_add_bug():
    project = Project("Website Redesign", owner_id="user123")
    project.add_bug("bug1")
    assert "bug1" in project.bugs

    # adding the same bug twice should not duplicate it
    project.add_bug("bug1")
    assert project.bugs.count("bug1") == 1


def test_remove_bug():
    project = Project("Website Redesign", owner_id="user123")
    project.add_bug("bug1")
    project.remove_bug("bug1")
    assert "bug1" not in project.bugs

    # removing something not present should not raise an error
    project.remove_bug("does_not_exist")


def test_to_dict_and_from_dict_roundtrip():
    project = Project("Mobile App", owner_id="user456")
    project.add_bug("bugA")
    project.add_bug("bugB")

    data = project.to_dict()
    assert data["name"] == "Mobile App"
    assert data["owner_id"] == "user456"
    assert data["bugs"] == ["bugA", "bugB"]

    rebuilt = Project.from_dict(data)
    assert rebuilt.id == project.id
    assert rebuilt.name == project.name
    assert rebuilt.owner_id == project.owner_id
    assert rebuilt.bugs == project.bugs
    assert rebuilt.created_at == project.created_at


def test_repr_contains_key_info():
    project = Project("API Refactor", owner_id="user789")
    text = repr(project)
    assert "API Refactor" in text
    assert "user789" in text
    assert project.id in text