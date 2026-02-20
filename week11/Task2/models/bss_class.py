from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BssClass(models.Model):
    _name = 'bss.class'
    _description = 'Class'
    _order = 'name'

    name = fields.Char(string="Class Name", required=True)
    code = fields.Char(string="Class Code", required=True)
    subject_ids = fields.Many2many('bss.subject', string="Subjects")

    # Replace _sql_constraints with Constraint
    _sql_constraints = [
        ('unique_class_code', 'unique(code)', 'The class code must be unique!')
    ]

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.code})"