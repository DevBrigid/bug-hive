from models.Bug import Bug

def test_bug_initialization():
    b = Bug(101, "API Timeout", "Backend", "high")
    assert b.bug_id == 101
    assert b.status == "open"

def test_resolution_flow():
    b = Bug(101, "API Timeout", "Backend", "high")
    assert b.resolve() is True
    assert b.status == "resolved"
    assert b.resolved_at is not None
    
    # Resolving again should change nothing
    assert b.resolve() is False