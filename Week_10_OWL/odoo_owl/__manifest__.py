{
    "name" : "Owl Counter",
    "version" : "0.1",
    "category" : "Tools",
    "summary" : "Owl module",
    "depends" : ["base", "web"],
    "data" : [
        "views/owl_menu.xml",
    ],
    "assets" : {
        "web.assets_backend" : [
            "odoo_owl/static/src/js/owl.js",
            "odoo_owl/static/src/xml/owl.xml",

        ],
    },
    "installable" : True,
    "application" : True,
}