from odoo import models, fields

class BssSubject(models.Model):
    _name = "bss.subject"
    _description = "Subject"

    name = fields.Char(string="Subject Name",required=True)
    code = fields.Char()
    total_sessions = fields.Integer(string="Total Sessions", default=0)  # NEW
