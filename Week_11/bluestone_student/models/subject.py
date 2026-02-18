from odoo import models, fields

class BssSubject(models.Model):
    _name = "bss.subject"
    _description = "Subject"

    name = fields.Char(required=True)
    code = fields.Char()
