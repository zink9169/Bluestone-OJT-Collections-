{
    'name': 'Real estate',
    'version': '1.0.0',
    'summary': 'For managing property',
    'description': 'For property market',
    'author': 'Mg Kyaw',
    'website': 'www.mgkyaw.com',
    'category': 'Sales',
    'sequence': -100,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}