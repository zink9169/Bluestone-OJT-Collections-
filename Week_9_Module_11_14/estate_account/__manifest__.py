{
    'name': 'Real Estate Accounting',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Generate invoices for sold properties',
    'description': """
        Link module between Real Estate and Accounting.
        Creates invoices automatically when properties are sold.
    """,
    'depends': ['estate', 'account'],
    'data': [
        # No views or security files needed for this simple module
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}