{
    'name': 'BSS Student Access Right',
    'version': '1.0',
    'depends': ['student'],   # your main module technical name
    'data': [
        'security/student_groups.xml',
        'security/ir.model.access.csv',
        'security/student_record_rules.xml',
    ],
    'installable': True,
}