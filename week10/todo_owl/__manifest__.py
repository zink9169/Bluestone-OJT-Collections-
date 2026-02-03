{
    "name": "OWL Todo List",
    "version": "1.0",
    "depends": ["web"],
    "data": [
        "views/todo_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "todo_owl/static/src/js/todo/todo.js",
            "todo_owl/static/src/js/todo/todo.xml",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}