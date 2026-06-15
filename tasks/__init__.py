# Cleanly expose service actions for the CLI layer to import directly
from .user_tasks import (
    create_user_task, 
    get_all_users_task
)

from .project_tasks import (
    create_project_task, 
    assign_user_to_project_task, 
    list_projects_task
)

from .bug_tasks import (
    report_bug_task, 
    resolve_bug_task, 
    list_bugs_task, 
    get_leaderboard_task
)