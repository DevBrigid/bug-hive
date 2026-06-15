from models.Gamification import Gamification

def test_xp_and_level_increments():
    g = Gamification("David")
    summary = g.award_xp_for_severity("high")  # +80 XP
    assert g.xp == 80
    assert g.level == 1
    assert summary["xp_gained"] == 80

def test_milestone_badge_unlocks():
    g = Gamification("Dev_Pro")
    # Simulate hitting milestones
    g.xp = 520
    summary = g.award_xp_for_severity("medium")  # Triggers milestone checks
    
    assert "Bug Scout" in g.badges
    assert "💻 Developer" in g.badges
    assert "💀 Exterminator" not in g.badges  # Requires 1000 XP