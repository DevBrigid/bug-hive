from storage import load_db, save_db
from models.Bug import Bug
from models.Gamification import Gamification

def report_bug_task(title, project_name, severity, assign_string):
    # Increments index counters and registers a new bug entity.
    db = load_db()
    if project_name not in db["projects"]:
        return {"success": False, "message": f"Project target '{project_name}' does not exist."}
    
    db["bug_counter"] += 1
    new_id = db["bug_counter"]
    assignees = [a.strip() for a in assign_string.split(",")] if assign_string else []
    
    bug = Bug(new_id, title, project_name, severity, assignees)
    db["bugs"][str(new_id)] = bug.to_dict()
    save_db(db)
    return {"success": True, "message": f"Ticket #{new_id} ('{title}') logged against [{project_name}]."}

def resolve_bug_task(bug_id):
    # Closes bug tickers and applies gamified progression deltas to developers.
    db = load_db()
    if str(bug_id) not in db["bugs"]:
        return {"success": False, "message": f"Bug verification check failed for ticket ID #{bug_id}."}
    
    bug = Bug.from_dict(db["bugs"][str(bug_id)])
    if not bug.resolve():
        return {"success": False, "message": f"Bug #{bug_id} has already been marked resolved."}
    
    db["bugs"][str(bug_id)] = bug.to_dict()
    rewards_payout = []
    
    for user in bug.assignees:
        if user in db["gamification"]:
            profile = Gamification.from_dict(user, db["gamification"][user])
            summary = profile.award_xp_for_severity(bug.severity)
            db["gamification"][user] = profile.to_dict()
            
            rewards_payout.append({
                "username": user,
                "xp_gained": summary["xp_gained"],
                "leveled_up": summary["leveled_up"],
                "new_level": profile.level,
                "badges_earned": summary["badges_earned"]
            })
            
    save_db(db)
    return {"success": True, "bug": bug, "rewards": rewards_payout}

def list_bugs_task(status=None, severity=None, search=None):
    # Applies conditional filtering passes onto saved bug entities.
    db = load_db()
    results = []
    for b in db["bugs"].values():
        bug = Bug.from_dict(b)
        if status and bug.status != status:
            continue
        if severity and bug.severity != severity:
            continue
        if search and search.lower() not in bug.title.lower():
            continue
        results.append(bug)
    return results

def get_leaderboard_task():
    # Extracts, maps, and ranks developer statistics descending by XP.
    db = load_db()
    profiles = [Gamification.from_dict(k, v) for k, v in db["gamification"].items()]
    profiles.sort(key=lambda x: x.xp, reverse=True)
    return profiles

def assign_bug_task(bug_id, assign_string):
    # Updates bug assignments to new developers.
    db = load_db()
    if str(bug_id) not in db["bugs"]:
        return {"success": False, "message": f"Bug verification check failed for ticket ID #{bug_id}."}
    
    bug = Bug.from_dict(db["bugs"][str(bug_id)])
    assignees = [a.strip() for a in assign_string.split(",")] if assign_string else []
    
    # Validate that all assignees exist
    for assignee in assignees:
        if assignee not in db["users"]:
            return {"success": False, "message": f"User '{assignee}' not found in system."}
    
    bug.assignees = assignees
    db["bugs"][str(bug_id)] = bug.to_dict()
    save_db(db)
    
    assignee_list = ", ".join(assignees) if assignees else "None"
    return {"success": True, "message": f"Ticket #{bug_id} reassigned to: {assignee_list}"}