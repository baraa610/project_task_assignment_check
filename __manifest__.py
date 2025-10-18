{
    "name": "Project Task Availability",
    "version": "1.0",
    "category": "Project",
    "summary": "Control assignment of tasks to users who are on leave or busy",
    "description": """
        - Warn or block task assignment if the user is on leave or busy with another task.
        - Support override with mandatory reason.
        - Configurable behavior from Project settings.
    """,
    "author": "Mohamed Hussein",
    "depends": ["project", "hr", "hr_holidays", "account"],
    "data": [
        "views/project_task_views.xml",
        "views/project_settings_views.xml",
        "data/project_task_assignment_data.xml",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
