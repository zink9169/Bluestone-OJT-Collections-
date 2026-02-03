{
    'name': 'My Todo App',
    'version': '1.0',
    'category': 'Tutorial',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'todo_app/static/src/components/todo_app.js',
            'todo_app/static/src/components/todo_app.xml',
            'todo_app/static/src/main.js',
        ],
    },
    'data': [
        'views/todo_view.xml',
    ],
    'installable': True,
    'application': True,
}
