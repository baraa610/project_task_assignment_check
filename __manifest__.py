{
    "name": "Project Planning Sync",
    "version": "1.0",
    "category": "Project",
    "summary": "Synchronize Project Tasks with Planning Slots",
    "description": "Automatically syncs project.task with planning.slot: create, update, delete.",
    "author": "Mohamed Hussein",
    "license": "LGPL-3",
    "depends": ["project", "planning"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
        "views/settings_views.xml",
        "data/project_planning_sync_data.xml",
    ],
    "installable": True,
    "application": False,
}
