{
    'name': "Awesome Owl",
    'version': '1.0',
    'category': 'OJT',
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            'awesome_owl/static/src/**/*',
        ],
    },
    'data': [
        'views/views.xml',
    ],
    'license': 'LGPL-3',
}
