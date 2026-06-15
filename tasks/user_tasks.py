from storage import load_db, save_db
from models.User import User
from models.Gamification import Gamification

def create_user_task(username, role):
    """Orchestrates adding a user and preparing gamification states if developer."""
    db = load_db()
    if username in db["users"]:
        return {"success": False, "message": f"The username '{username}' already exists."}
    
    user = User(username, role)
    db["users"][username] = user.to_dict()
    
    if role == "developer":
        db["gamification"][username] = Gamification(username).to_dict()
        
    save_db(db)
    return {"success": True, "message": f"Registered {username} as a team '{role}'."}

def get_all_users_task():
    """Retrieves all raw user data rows from persistence."""
    db = load_db()
    return list(db["users"].values())