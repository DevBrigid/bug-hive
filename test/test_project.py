from models.Project import Project

def test_project_initialization():
    p = Project("Web UI", "Redesigning assets")
    assert p.name == "Web UI"
    assert len(p.members) == 0

def test_assign_user():
    p = Project("Web UI", "Redesigning assets")
    assert p.assign_user("Charlie") is True
    assert "Charlie" in p.members
    
    # Block duplication
    assert p.assign_user("Charlie") is False