from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BssClass(models.Model):
    _name = "bss.class"
    _description = "Class"

    name = fields.Char(required=True)
    code = fields.Char(required=True)

    subject_ids = fields.Many2many("bss.subject", string="Subjects")

    _sql_constraints = [
        ("unique_code", "unique(code)", "Code must be unique!")
    ]

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} ({record.code})"
            result.append((record.id, name))
        return result
