class Gamification:
    def __init__(self, username, xp=0, level=1, badges=None):
        self.username = username
        self.xp = xp
        self.level = level
        self.badges = badges if badges is not None else []

    def award_xp_for_severity(self, severity):
        xp_map = {"low": 20, "medium": 50, "high": 80}
        reward = xp_map.get(severity.lower(), 20)
        self.xp += reward
        
        # Level up threshold rules (Every 200 XP = 1 Level)
        new_level = (self.xp // 200) + 1
        leveled_up = new_level > self.level
        self.level = new_level

        # Milestone badges checks
        new_badges = []
        milestones = [
            (100, "Bug Scout"),
            (500, "Developer"),
            (1000, "Exterminator")
        ]
        for milestone_xp, badge_name in milestones:
            if self.xp >= milestone_xp and badge_name not in self.badges:
                self.badges.append(badge_name)
                new_badges.append(badge_name)

        return {"xp_gained": reward, "leveled_up": leveled_up, "badges_earned": new_badges}

    def to_dict(self):
        return {"username": self.username, "xp": self.xp, "level": self.level, "badges": self.badges}

    @staticmethod
    def from_dict(username, data):
        if not data:
            return Gamification(username)
        return Gamification(username, data.get("xp", 0), data.get("level", 1), data.get("badges", []))