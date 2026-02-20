from odoo import models, fields

class BssClass(models.Model):
    _name = 'bss.class'
    _description = 'Class'

    name = fields.Char(string="Class Name", required=True)
    code = fields.Char(string="Class Code")
    subject_ids = fields.Many2many('bss.subject', string="Subjects")
    description = fields.Text(string="Description")