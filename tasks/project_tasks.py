from storage import load_db, save_db
from models.Project import Project

def create_project_task(name, description):
    # Initializes a new tracking workspace.
    db = load_db()
    if name in db["projects"]:
        return {"success": False, "message": f"Project '{name}' already exists."}
    
    proj = Project(name, description)
    db["projects"][name] = proj.to_dict()
    save_db(db)
    return {"success": True, "message": f"Workspace '{name}' created successfully."}

def assign_user_to_project_task(project_name, username):
    # Validates existence and appends a team member to a project.
    db = load_db()
    if project_name not in db["projects"] or username not in db["users"]:
        return {"success": False, "message": "Target Project or Username parameters not found."}
    
    proj = Project.from_dict(db["projects"][project_name])
    if proj.assign_user(username):
        db["projects"][project_name] = proj.to_dict()
        save_db(db)
        return {"success": True, "message": f"User '{username}' assigned to '{project_name}'."}
    
    return {"success": False, "message": f"{username} is already assigned to this project."}

def list_projects_task(owner_filter=None):
    # Filters and aggregates current project schemas.
    db = load_db()
    results = []
    for p in db["projects"].values():
        proj = Project.from_dict(p)
        if owner_filter and owner_filter not in proj.members:
            continue
        results.append(proj)
    return results