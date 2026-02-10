{
    "name": "Project Task Dashboard",
    "version": "1.0",
    "depends": ["project", "web", "base"],
    "data" : [
        "views/project_task_dashboard_action.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "project_task_dashboard/static/src/js/task_dashboard.js",
            "project_task_dashboard/static/src/xml/task_dashboard.xml",
            "project_task_dashboard/static/src/css/task_dashboard.scss",
        ]
    }
}
