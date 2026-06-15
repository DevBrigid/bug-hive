# BugHive 🐝

A gamified bug tracking and project management CLI tool with role-based authentication and real-time collaboration features.

## Features

- ** Authentication**: Role-based access control with Admin and Developer profiles
- ** Gamification**: Leaderboard system, points for bug resolutions, and achievement tracking
- ** Bug Management**: Report, track, and resolve bugs with severity levels and assignees
- ** Project Management**: Create and manage projects with team member assignments
- ** User Management**: Admin capabilities for user creation and role management
- ** Persistent Storage**: JSON-based data persistence for all records

## Installation

### Requirements
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/DevBrigid/bug-hive.git
cd BugHive
```

2. Install dependencies using requirements.txt:
```bash
pip install -r requirements.txt
```

**OR** install the package in development mode:
```bash
pip install -e .
```

3. Activate the virtual environment (if using one):
```bash
source .bughive/bin/activate  # On Linux/Mac
```

## Usage

### Authentication

**Login:**
```bash
bughive login <username>
```

**Logout:**
```bash
bughive logout
```

### User Management (Admin Only)

**Create a new user:**
```bash
bughive user add <username> <role>
```
Roles: `admin`, `developer`

**List all users:**
```bash
bughive user list
```

**Delete a user:**
```bash
bughive user delete <username>
```

### Project Management

**Create a project:**
```bash
bughive project create <project_name> <prjoect_description> #optional
```

**List projects:**
```bash
bughive project list
```

**Assign user to project:**
```bash
bughive project assign <username> <project_name>
```

### Bug Management

**Report a bug:**
```bash
bughive bug report <title> <project_name> [--severity <level>] [--assign <assignees>]
```
Severity levels: `low`, `medium` (default), `high`

**Examples:**
```bash
bughive bug report "Login page failing" "Mobile Core" --severity high
bughive bug report "Missing button" "Mobile Core" --severity medium --assign user1,user2
```

**List bugs:**
```bash
bughive bug list [project_name]
```

**Assign developers to a bug:**
```bash
bughive bug assign <bug_id> <assignees>
```
Assignees: Comma-separated list of usernames

**Examples:**
```bash
bughive bug assign 1 john_dev
bughive bug assign 1 john_dev,jane_dev,alex_dev
```

**Resolve a bug:**
```bash
bughive bug resolve <bug_id>
```

### Gamification

**View leaderboard:**
```bash
bughive leaderboard
```

## Project Structure

```
BugHive/
├── cli.py                 # Main CLI interface
├── storage.py             # Data persistence layer
├── db.json               # JSON database file
├── setup.py              # Package configuration
├── requirements.txt      # Python dependencies
├── models/               # Data models
│   ├── User.py          # User model with roles
│   ├── Bug.py           # Bug tracking model
│   ├── Project.py       # Project management model
│   └── Gamification.py  # Gamification system
├── tasks/               # Business logic
│   ├── auth_task.py     # Authentication logic
│   ├── user_tasks.py    # User management
│   ├── bug_tasks.py     # Bug operations
│   └── project_tasks.py # Project operations
├── test/                # Unit tests
│   ├── test_user.py
│   ├── test_bug.py
│   ├── test_project.py
│   └── test_gamification.py
└── README.md            # Project documentation
```

## Architecture

### Authentication System
- Session-based login with role validation
- Two roles: **Admin** (full access) and **Developer** (limited access)
- Admin commands: user creation, user deletion, project assignment
- Developer commands: bug reporting, bug resolution viewing

### Database
- JSON-based persistent storage in `db.json`
- Stores users, projects, bugs, and gamification data
- Auto-synchronized on each operation

### Gamification
- Points awarded for bug resolutions
- Leaderboard tracking top developers
- Encourages collaboration and productivity

## Commands Reference

| Command | Role | Description |
|---------|------|-------------|
| `login` | Any | Authenticate with username |
| `logout` | Any | Clear session |
| `user add` | Admin | Create new user |
| `user list` | Admin | List all users |
| `user delete` | Admin | Delete a user |
| `project create` | Any | Create project |
| `project list` | Any | List projects |
| `project assign` | Admin | Assign user to project |
| `bug report` | Dev | Report a bug |
| `bug list` | Any | List bugs |
| `bug resolve` | Dev | Mark bug as resolved |
| `leaderboard` | Any | View top performers |

## Testing

Run the test suite:
```bash
pytest test/
```

Run specific test file:
```bash
pytest test/test_bug.py -v
```

## Development

### Adding New Commands

1. Create a task function in `tasks/` folder
2. Import the function in `cli.py`
3. Create a Click command decorator and call the task
4. Update the model if needed in `models/`

### Code Style

- Follow PEP 8 standards
- Use type hints where possible
- Add docstrings to functions and classes

## Dependencies

- **click**: CLI framework
- **tabulate**: Table formatting for output
- **colorama**: Colored terminal output
- **pytest**: Testing framework

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please open an issue on the repository.
