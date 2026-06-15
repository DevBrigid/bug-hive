from storage import load_db, save_db

def login_task(username):
    # Authenticates a user and sets the active session.
    db = load_db()
    if username not in db["users"]:
        return {"success": False, "message": f"User '{username}' does not exist."}
    
    db["current_session"] = username
    save_db(db)
    role = db["users"][username]["role"]
    return {"success": True, "message": f"Welcome back, {username}! Logged in as [{role.upper()}]."}

def logout_task():
    # Clears the active session.
    db = load_db()
    if not db["current_session"]:
        return {"success": False, "message": "No active session found."}
    
    old_user = db["current_session"]
    db["current_session"] = None
    save_db(db)
    return {"success": True, "message": f"Goodbye, {old_user}! Logged out successfully."}

def get_current_user_or_raise():
    # Helper framework rule to verify if a user is logged in and returns their profile.
    db = load_db()
    username = db.get("current_session")
    if not username or username not in db["users"]:
        return None
    return db["users"][username]