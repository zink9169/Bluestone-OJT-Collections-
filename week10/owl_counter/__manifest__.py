{
    "name": "OWL Counter App",
    "version": "1.0",
    "depends": ["web"],
    "data": [
        "views/assets.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "owl_counter/static/src/js/counter.js",
            "owl_counter/static/src/xml/counter.xml",
        ],
    },
    "installable": True,
    "application": True,
}
