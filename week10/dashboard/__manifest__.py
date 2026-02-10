{
    'name': 'Project Dashboard',
    'version': '1.0',
    'category': 'Project',
    'depends': ['project', 'web'],
    'data': [
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_project_dashboard/static/src/components/dashboard.js',
            'custom_project_dashboard/static/src/components/dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}