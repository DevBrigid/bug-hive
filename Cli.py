import argparse
import sys

from rich.console import Console
from rich.table import Table

from storage import Storage
from models.User import User
from models.Project import Project
from models.Bug import Bug


console = Console()


# Helper — resolve a user/project/bug by ID OR by name (case-insensitive)

def resolve_user(storage, identifier):
    user = storage.get_user_by_id(identifier) or storage.get_user_by_name(identifier)
    return user


def resolve_project(storage, identifier):
    project = storage.get_project_by_id(identifier) or storage.get_project_by_name(identifier)
    return project


def resolve_bug(storage, identifier):
    return storage.get_bug_by_id(identifier)


# USER commands

def cmd_add_user(args, storage):
    if storage.get_user_by_name(args.name):
        console.print(f"[red]A user named '{args.name}' already exists.[/red]")
        return

    user = User(name=args.name, role=args.role)
    storage.add_user(user)
    storage.save()

    console.print(f"[green]User created:[/green] {user.name} "
                   f"(role: [bold]{user.role}[/bold], id: {user.id})")


def cmd_list_users(args, storage):
    if not storage.users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Role", style="magenta")
    table.add_column("Projects", style="green")

    for user in storage.users:
        table.add_row(user.id, user.name, user.role, str(len(user.projects)))

    console.print(table)


# PROJECT commands

def cmd_add_project(args, storage):
    owner = resolve_user(storage, args.owner)
    if not owner:
        console.print(f"[red]No user found matching '{args.owner}'.[/red]")
        return

    if storage.get_project_by_name(args.name):
        console.print(f"[red]A project named '{args.name}' already exists.[/red]")
        return

    project = Project(name=args.name, owner_id=owner.id)
    storage.add_project(project)
    owner.assign_project(project.id)        # keep the relationship in sync
    storage.save()

    console.print(f"[green]Project created:[/green] {project.name} "
                   f"(owner: [bold]{owner.name}[/bold], id: {project.id})")


def cmd_list_projects(args, storage):
    projects = storage.projects

    if args.user:
        owner = resolve_user(storage, args.user)
        if not owner:
            console.print(f"[red]No user found matching '{args.user}'.[/red]")
            return
        projects = storage.get_projects_by_user(owner.id)

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Owner", style="magenta")
    table.add_column("Bugs", style="green")
    table.add_column("Created", style="dim")

    for project in projects:
        owner = storage.get_user_by_id(project.owner_id)
        owner_name = owner.name if owner else "unknown"
        table.add_row(project.id, project.name, owner_name,
                       str(len(project.bugs)), project.created_at)

    console.print(table)


#BUG commands

def cmd_add_bug(args, storage):
    project = resolve_project(storage, args.project)
    if not project:
        console.print(f"[red]No project found matching '{args.project}'.[/red]")
        return

    try:
        bug = Bug(
            title=args.title,
            description=args.description or "",
            severity=args.severity,
            project_id=project.id,
        )
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        return

    storage.add_bug(bug)
    project.add_bug(bug.id)                  # keep the relationship in sync
    storage.save()

    severity_color = {"low": "green", "medium": "yellow", "high": "red"}[bug.severity]
    console.print(f"[green]Bug reported:[/green] {bug.title} "
                   f"(severity: [{severity_color}]{bug.severity}[/{severity_color}], "
                   f"project: [bold]{project.name}[/bold], id: {bug.id})")


def cmd_assign_bug(args, storage):
    bug = resolve_bug(storage, args.bug_id)
    if not bug:
        console.print(f"[red]No bug found with id '{args.bug_id}'.[/red]")
        return

    user = resolve_user(storage, args.to)
    if not user:
        console.print(f"[red]No user found matching '{args.to}'.[/red]")
        return

    bug.assign(user.id)
    storage.save()

    console.print(f"[green]{user.name}[/green] assigned to bug "
                   f"'[bold]{bug.title}[/bold]' (id: {bug.id})")


def cmd_resolve_bug(args, storage):
    bug = resolve_bug(storage, args.bug_id)
    if not bug:
        console.print(f"[red]No bug found with id '{args.bug_id}'.[/red]")
        return

    if bug.status == "resolved":
        console.print(f"[yellow]Bug '{bug.title}' is already resolved.[/yellow]")
        return

    bug.resolve()
    storage.save()

    console.print(f"[green]Bug resolved:[/green] {bug.title} "
                   f"(resolved on {bug.resolved_at})")


def cmd_reopen_bug(args, storage):
    bug = resolve_bug(storage, args.bug_id)
    if not bug:
        console.print(f"[red]No bug found with id '{args.bug_id}'.[/red]")
        return

    if bug.status == "open":
        console.print(f"[yellow]Bug '{bug.title}' is already open.[/yellow]")
        return

    bug.reopen()
    storage.save()

    console.print(f"[green]Bug reopened:[/green] {bug.title}")


def cmd_list_bugs(args, storage):
    bugs = storage.bugs

    if args.project:
        project = resolve_project(storage, args.project)
        if not project:
            console.print(f"[red]No project found matching '{args.project}'.[/red]")
            return
        bugs = storage.get_bugs_by_project(project.id)

    if args.status:
        bugs = [b for b in bugs if b.status == args.status]

    if args.severity:
        bugs = [b for b in bugs if b.severity == args.severity]

    _print_bug_table(storage, bugs, title="Bugs")


def cmd_search_bugs(args, storage):
    bugs = storage.search_bugs(args.keyword)
    _print_bug_table(storage, bugs, title=f"Search results for '{args.keyword}'")


def _print_bug_table(storage, bugs, title="Bugs"):
    if not bugs:
        console.print("[yellow]No bugs found.[/yellow]")
        return

    table = Table(title=title)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Severity")
    table.add_column("Status")
    table.add_column("Project", style="magenta")
    table.add_column("Assignees", style="green")

    severity_color = {"low": "green", "medium": "yellow", "high": "red"}
    status_color = {"open": "red", "resolved": "green"}

    for bug in bugs:
        project = storage.get_project_by_id(bug.project_id)
        project_name = project.name if project else "unknown"

        assignee_names = []
        for uid in bug.assignees:
            user = storage.get_user_by_id(uid)
            assignee_names.append(user.name if user else uid)

        sev_style = severity_color.get(bug.severity, "white")
        status_style = status_color.get(bug.status, "white")

        table.add_row(
            bug.id,
            bug.title,
            f"[{sev_style}]{bug.severity}[/{sev_style}]",
            f"[{status_style}]{bug.status}[/{status_style}]",
            project_name,
            ", ".join(assignee_names) if assignee_names else "-",
        )

    console.print(table)


# Argument parser setup

def build_parser():
    parser = argparse.ArgumentParser(
        prog="bughive",
        description="BugHive — a CLI bug tracker for development teams.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- add ---
    add_parser = subparsers.add_parser("add", help="Add a user, project, or bug")
    add_subparsers = add_parser.add_subparsers(dest="entity")

    add_user = add_subparsers.add_parser("user", help="Add a new user")
    add_user.add_argument("--name", required=True, help="Name of the user")
    add_user.add_argument("--role", choices=User.VALID_ROLES, default="developer",
                           help="Role of the user (default: developer)")
    add_user.set_defaults(func=cmd_add_user)

    add_project = add_subparsers.add_parser("project", help="Add a new project")
    add_project.add_argument("--name", required=True, help="Name of the project")
    add_project.add_argument("--owner", required=True,
                              help="Owner's user ID or name")
    add_project.set_defaults(func=cmd_add_project)

    add_bug = add_subparsers.add_parser("bug", help="Report a new bug")
    add_bug.add_argument("--title", required=True, help="Bug title")
    add_bug.add_argument("--description", default="", help="Bug description")
    add_bug.add_argument("--severity", choices=Bug.VALID_SEVERITIES, default="medium",
                          help="Bug severity (default: medium)")
    add_bug.add_argument("--project", required=True, help="Project ID or name")
    add_bug.set_defaults(func=cmd_add_bug)

    # --- list ---
    list_parser = subparsers.add_parser("list", help="List users, projects, or bugs")
    list_subparsers = list_parser.add_subparsers(dest="entity")

    list_users = list_subparsers.add_parser("users", help="List all users")
    list_users.set_defaults(func=cmd_list_users)

    list_projects = list_subparsers.add_parser("projects", help="List projects")
    list_projects.add_argument("--user", help="Filter by owner's user ID or name")
    list_projects.set_defaults(func=cmd_list_projects)

    list_bugs = list_subparsers.add_parser("bugs", help="List bugs")
    list_bugs.add_argument("--project", help="Filter by project ID or name")
    list_bugs.add_argument("--status", choices=Bug.VALID_STATUSES, help="Filter by status")
    list_bugs.add_argument("--severity", choices=Bug.VALID_SEVERITIES, help="Filter by severity")
    list_bugs.set_defaults(func=cmd_list_bugs)

    # --- assign ---
    assign_parser = subparsers.add_parser("assign", help="Assign a bug to a developer")
    assign_subparsers = assign_parser.add_subparsers(dest="entity")

    assign_bug = assign_subparsers.add_parser("bug", help="Assign a bug to a user")
    assign_bug.add_argument("bug_id", help="ID of the bug")
    assign_bug.add_argument("--to", required=True, help="User ID or name to assign")
    assign_bug.set_defaults(func=cmd_assign_bug)

    # --- resolve ---
    resolve_parser = subparsers.add_parser("resolve", help="Mark a bug as resolved")
    resolve_subparsers = resolve_parser.add_subparsers(dest="entity")

    resolve_bug_p = resolve_subparsers.add_parser("bug", help="Resolve a bug")
    resolve_bug_p.add_argument("bug_id", help="ID of the bug")
    resolve_bug_p.set_defaults(func=cmd_resolve_bug)

    # --- reopen ---
    reopen_parser = subparsers.add_parser("reopen", help="Reopen a resolved bug")
    reopen_subparsers = reopen_parser.add_subparsers(dest="entity")

    reopen_bug_p = reopen_subparsers.add_parser("bug", help="Reopen a bug")
    reopen_bug_p.add_argument("bug_id", help="ID of the bug")
    reopen_bug_p.set_defaults(func=cmd_reopen_bug)

    # --- search ---
    search_parser = subparsers.add_parser("search", help="Search bugs by keyword")
    search_subparsers = search_parser.add_subparsers(dest="entity")

    search_bugs = search_subparsers.add_parser("bugs", help="Search bugs by title keyword")
    search_bugs.add_argument("--keyword", required=True, help="Keyword to search for")
    search_bugs.set_defaults(func=cmd_search_bugs)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    storage = Storage()
    storage.load()

    args.func(args, storage)


if __name__ == "__main__":
    main()