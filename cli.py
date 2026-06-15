import click
from tabulate import tabulate
from colorama import Fore, Style, init

from tasks import (
    create_user_task, get_all_users_task, delete_user_task,
    create_project_task, assign_user_to_project_task, list_projects_task,
    report_bug_task, resolve_bug_task, list_bugs_task, get_leaderboard_task, assign_bug_task,
    login_task, logout_task, get_current_user_or_raise
)

init(autoreset=True)

# Helper function to enforce role rules easily
def enforce_role(required_role=None):
    # Checks the active session and validates role clearance.
    user = get_current_user_or_raise()
    if not user:
        click.echo(Fore.RED + " Access Denied: You must be logged in to perform this action. Run: bughive login [username]")
        ctx = click.get_current_context()
        ctx.exit()
    
    if required_role and user["role"] != required_role:
        click.echo(Fore.RED + f" Permission Denied: This command requires an [{required_role.upper()}] role. You are a [{user['role'].upper()}].")
        ctx = click.get_current_context()
        ctx.exit()
    return user

@click.group()
def bughive():
    # BugHive CLI Tool: Gamified task management with role-based authentication.
    pass

# AUTHENTICATION COMMANDS
@bughive.command(name="login")
@click.argument("username")
def login(username):
    # Authenticate into your BugHive developer/admin profile workspace.
    res = login_task(username)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

@bughive.command(name="logout")
def logout():
    # Clear the active terminal profile session safely.
    res = logout_task()
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

# USER SUBSYSTEM (ADMIN ONLY)
@bughive.group(name="user")
def user_group():
    # User profile control panel.
    pass

@user_group.command(name="add")
@click.argument("username")
@click.argument("role", type=click.Choice(["admin", "developer"]))
def add_user(username, role):
    enforce_role(required_role="admin") # Guard check
    res = create_user_task(username, role)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

@user_group.command(name="list")
def list_users():
    enforce_role() # Must be logged in, either admin or dev
    users = get_all_users_task()
    if not users:
        click.echo(Fore.YELLOW + "No user records found.")
        return
    table = [[u["username"], u["role"]] for u in users]
    click.echo(tabulate(table, headers=["Username", "System Role"], tablefmt="fancy_grid"))

@user_group.command(name="delete")
@click.argument("username")
def delete_user(username):
    enforce_role(required_role="admin") # Guard check
    res = delete_user_task(username)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

# PROJECT SUBSYSTEM (ADMIN ONLY FOR MUTATIONS)
@bughive.group(name="project")
def project_group():
    # Project workspaces allocation control panel.
    pass

@project_group.command(name="create")
@click.argument("name")
@click.argument("description")
def create_project(name, description):
    enforce_role(required_role="admin") # Guard check
    res = create_project_task(name, description)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

@project_group.command(name="assign")
@click.argument("project_name")
@click.argument("username")
def assign_user(project_name, username):
    enforce_role(required_role="admin") # Guard check
    res = assign_user_to_project_task(project_name, username)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

@project_group.command(name="list")
@click.option("--owner", help="Filter tracking by assigned worker.")
def list_projects(owner):
    enforce_role() # Anyone authenticated can read
    projects = list_projects_task(owner)
    if not projects:
        click.echo(Fore.YELLOW + "No projects matching evaluation matrices found.")
        return
    table = [[p.name, p.description, ", ".join(p.members) or "None"] for p in projects]
    click.echo(tabulate(table, headers=["Project Name", "Description", "Assigned Staff"], tablefmt="fancy_grid"))

# BUG SUBSYSTEM (OPEN TO LOGGED IN USERS)
@bughive.group(name="bug")
def bug_group():
    # Bug tracking mechanics.
    pass

@bug_group.command(name="report")
@click.argument("title")
@click.argument("project_name")
@click.option("--severity", default="medium", type=click.Choice(["low", "medium", "high"]))
@click.option("--assign", help="Comma-separated assignees names.")
def report_bug(title, project_name, severity, assign):
    enforce_role() # Anyone logged in can file a bug report
    res = report_bug_task(title, project_name, severity, assign)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

@bug_group.command(name="resolve")
@click.argument("bug_id", type=int)
def resolve_bug(bug_id):
    enforce_role(required_role="developer") # ONLY developers can resolve bugs for XP!
    res = resolve_bug_task(bug_id)
    if not res["success"]:
        click.echo(Fore.RED + res["message"])
        return
        
    click.echo(Fore.CYAN + f"Ticket closed! Processing rewards...")
    for rew in res["rewards"]:
        click.echo(Fore.WHITE + f" -> {rew['username']} received +{rew['xp_gained']} XP.")
        if rew["leveled_up"]:
            click.echo(Fore.GREEN + Style.BRIGHT + f"   🌟 LEVEL UP! Scaled to Level {rew['new_level']}!")
        for badge in rew["badges_earned"]:
            click.echo(Fore.MAGENTA + Style.BRIGHT + f"   🏆 ACHIEVEMENT UNLOCKED: [{badge}]!")

@bug_group.command(name="list")
@click.option("--status", type=click.Choice(["open", "resolved"]))
@click.option("--severity", type=click.Choice(["low", "medium", "high"]))
@click.option("--search", help="Title keyword substring matches.")
def list_bugs(status, severity, search):
    enforce_role()
    bugs = list_bugs_task(status, severity, search)
    if not bugs:
        click.echo(Fore.YELLOW + "No matching bug issues tracked.")
        return
    table = [[b.bug_id, b.title, b.project_name, b.severity.upper(), b.status, ", ".join(b.assignees)] for b in bugs]
    click.echo(tabulate(table, headers=["ID", "Title Summary", "Project", "Priority", "Status", "Workers"], tablefmt="fancy_grid"))

@bug_group.command(name="assign")
@click.argument("bug_id", type=int)
@click.argument("assignees")
def assign_bug(bug_id, assignees):
    enforce_role() # Anyone logged in can reassign bugs
    res = assign_bug_task(bug_id, assignees)
    color = Fore.GREEN if res["success"] else Fore.RED
    click.echo(color + res["message"])

# LEADERBOARD
@bughive.command(name="leaderboard")
def leaderboard():
    enforce_role()
    profiles = get_leaderboard_task()
    if not profiles:
        click.echo(Fore.YELLOW + "No registered developers found on active rank leaderboards.")
        return
    table = [[idx + 1, p.username, p.xp, p.level, ", ".join(p.badges) or "None"] for idx, p in enumerate(profiles)]
    click.echo(tabulate(table, headers=["Rank", "Developer", "XP Score", "Level", "Badges Ledger"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    bughive()