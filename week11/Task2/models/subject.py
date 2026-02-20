from odoo import models, fields


class BssSubject(models.Model):
    _name = 'bss.subject'
    _description = 'Subject'
    _order = 'name'

    name = fields.Char(string="Subject Name", required=True)

    class_ids = fields.Many2many(
        'bss.class',
        string="Classes"
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Subject name must be unique!')
    ]