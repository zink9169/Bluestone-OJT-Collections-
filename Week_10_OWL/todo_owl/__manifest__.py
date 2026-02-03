{
    "name": "Todo Owl",
    "version": "1.0",
    "depends": ["web"],
    "data": [
        "views/templates.xml",
        "views/menu.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "todo_owl/static/src/app.js",
            "todo_owl/static/src/app.xml",
            "todo_owl/static/src/css/todo.css",

            "todo_owl/static/src/components/todo_list.js",
            "todo_owl/static/src/components/todo_list.xml",

            "todo_owl/static/src/components/todo_item.js",
            "todo_owl/static/src/components/todo_item.xml",
        ]
    },

    "installable": True,
    "application": True
}
