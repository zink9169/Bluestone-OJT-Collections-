{
    'name': 'BSS School Task 3 - Student Access Rights',
    'version': '1.0',
    'author': 'hsumonsi',
    'license': 'LGPL-3',
    'category': 'Education',
    'summary': 'User security groups for student management',
    'description': """
        Adds two user roles for student management:
        - Student User: View only their own profile and attendance
        - Student Admin: Full access to all student data
    """,
    'depends': [ 'Task2'],
    'data': [
        'security/student_groups.xml',
        'security/student_record_rules.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}