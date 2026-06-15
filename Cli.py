import click
from tabulate import tabulate
from colorama import Fore, Style, init

from storage import load_db, save_db
from models.User import User
from models.Project import Project
from models.Bug import Bug
from models.Gamification import Gamification

# Initialize colorama for windows/unix global compatibility
init(autoreset=True)

@click.group()
def bughive():
    # BugHive CLI Tool: Gamified task management for small dev squads.
    pass

# USER SUBSYSTEM 
@bughive.group(name="user")
def user_group():
    # User profile control panel.
    pass

@user_group.command(name="add")
@click.argument("username")
@click.argument("role", type=click.Choice(["admin", "developer"]))
def add_user(username, role):
    db = load_db()
    if username in db["users"]:
        click.echo(Fore.RED + f"Error: The username '{username}' already exists.")
        return
    
    user = User(username, role)
    db["users"][username] = user.to_dict()
    # Initialize basic scoreboards instantly inside db profile storage
    if role == "developer":
        db["gamification"][username] = Gamification(username).to_dict()
        
    save_db(db)
    click.echo(Fore.GREEN + f"Success: Registered {username} as a team '{role}'.")

@user_group.command(name="list")
def list_users():
    db = load_db()
    if not db["users"]:
        click.echo(Fore.YELLOW + "No user records found.")
        return
    
    table_data = [[u["username"], u["role"]] for u in db["users"].values()]
    click.echo(tabulate(table_data, headers=["Username", "System Role"], tablefmt="fancy_grid"))

#  PROJECT SUBSYSTEM 
@bughive.group(name="project")
def project_group():
    """Project workspaces allocation control panel."""
    pass

@project_group.command(name="create")
@click.argument("name")
@click.argument("description")
def create_project(name, description):
    db = load_db()
    if name in db["projects"]:
        click.echo(Fore.RED + f"Error: Project '{name}' already exists.")
        return
    
    proj = Project(name, description)
    db["projects"][name] = proj.to_dict()
    save_db(db)
    click.echo(Fore.GREEN + f"Success: Workspace '{name}' created successfully.")

@project_group.command(name="assign")
@click.argument("project_name")
@click.argument("username")
def assign_user(project_name, username):
    db = load_db()
    if project_name not in db["projects"] or username not in db["users"]:
        click.echo(Fore.RED + "Error: Target Project or Username parameters not found.")
        return
    
    proj = Project.from_dict(db["projects"][project_name])
    if proj.assign_user(username):
        db["projects"][project_name] = proj.to_dict()
        save_db(db)
        click.echo(Fore.GREEN + f"Success: User '{username}' assigned to '{project_name}'.")
    else:
        click.echo(Fore.YELLOW + f"Notice: {username} is already assigned to this project.")

@project_group.command(name="list")
@click.option("--owner", help="Filter tracking by assigned worker.")
def list_projects(owner):
    db = load_db()
    table_data = []
    for p in db["projects"].values():
        proj = Project.from_dict(p)
        if owner and owner not in proj.members:
            continue
        table_data.append([proj.name, proj.description, ", ".join(proj.members) or "None"])
        
    if not table_data:
        click.echo(Fore.YELLOW + "No projects matching evaluation matrices found.")
    else:
        click.echo(tabulate(table_data, headers=["Project Name", "Description", "Assigned Staff"], tablefmt="fancy_grid"))

# BUG SUBSYSTEM

@bughive.group(name="bug")
def bug_group():
    """Bug tracking mechanics."""
    pass

@bug_group.command(name="report")
@click.argument("title")
@click.argument("project_name")
@click.option("--severity", default="medium", type=click.Choice(["low", "medium", "high"]))
@click.option("--assign", help="Comma-separated assignees names.")
def report_bug(title, project_name, severity, assign):
    db = load_db()
    if project_name not in db["projects"]:
        click.echo(Fore.RED + f"Error: Project workflow target '{project_name}' does not exist.")
        return
    
    db["bug_counter"] += 1
    new_id = db["bug_counter"]
    assignees = [a.strip() for a in assign.split(",")] if assign else []
    
    bug = Bug(new_id, title, project_name, severity, assignees)
    db["bugs"][str(new_id)] = bug.to_dict()
    save_db(db)
    click.echo(Fore.GREEN + f"Success: Ticket #{new_id} ('{title}') logged against [{project_name}].")

@bug_group.command(name="resolve")
@click.argument("bug_id", type=int)
def resolve_bug(bug_id):
    db = load_db()
    if str(bug_id) not in db["bugs"]:
        click.echo(Fore.RED + f"Error: Bug verification check failed for ticket ID #{bug_id}.")
        return
    
    bug = Bug.from_dict(db["bugs"][str(bug_id)])
    if not bug.resolve():
        click.echo(Fore.YELLOW + f"Notice: Bug #{bug_id} has already been marked resolved.")
        return
    
    db["bugs"][str(bug_id)] = bug.to_dict()
    click.echo(Fore.CYAN + f"Ticket closed! Calculating gamified reward shares for: {', '.join(bug.assignees)}")
    
    # Process game metrics engine payouts
    for user in bug.assignees:
        if user in db["gamification"]:
            profile = Gamification.from_dict(user, db["gamification"][user])
            summary = profile.award_xp_for_severity(bug.severity)
            db["gamification"][user] = profile.to_dict()
            
            click.echo(Fore.WHITE + f" -> {user} received +{summary['xp_gained']} XP.")
            if summary["leveled_up"]:
                click.echo(Fore.GREEN + Style.BRIGHT + f"   🌟 LEVEL UP! {user} scaled to Level {profile.level}!")
            for badge in summary["badges_earned"]:
                click.echo(Fore.MAGENTA + Style.BRIGHT + f"   🏆 ACHIEVEMENT UNLOCKED: [{badge}]!")
                
    save_db(db)

@bug_group.command(name="list")
@click.option("--status", type=click.Choice(["open", "resolved"]))
@click.option("--severity", type=click.Choice(["low", "medium", "high"]))
@click.option("--search", help="Title keyword substring matches.")
def list_bugs(status, severity, search):
    db = load_db()
    table_data = []
    for b in db["bugs"].values():
        bug = Bug.from_dict(b)
        if status and bug.status != status:
            continue
        if severity and bug.severity != severity:
            continue
        if search and search.lower() not in bug.title.lower():
            continue
        table_data.append([bug.bug_id, bug.title, bug.project_name, bug.severity.upper(), bug.status, ", ".join(bug.assignees)])
        
    if not table_data:
        click.echo(Fore.YELLOW + "No matching bug issues tracked under current parameter variants.")
    else:
        click.echo(tabulate(table_data, headers=["ID", "Title Summary", "Project", "Priority", "Status", "Workers"], tablefmt="fancy_grid"))

# GAMIFICATION SUBSYSTEM
@bughive.command(name="leaderboard")
def leaderboard():
    """Rank all developers based on current total experience tracking indices."""
    db = load_db()
    if not db["gamification"]:
        click.echo(Fore.YELLOW + "No registered developers found on active rank leaderboards.")
        return
    
    profiles = [Gamification.from_dict(k, v) for k, v in db["gamification"].items()]
    profiles.sort(key=lambda x: x.xp, reverse=True)
    
    table_data = [[idx + 1, p.username, p.xp, p.level, ", ".join(p.badges) or "None"] for idx, p in enumerate(profiles)]
    click.echo(tabulate(table_data, headers=["Rank", "Developer", "XP Score", "Level Title", "Badges Ledger"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    bughive()