from email.policy import default

from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    
    name = fields.Char(required=True)
    color = fields.Integer('Color Index', default=0)
    # === SQL CONSTRAINTS ===
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'Tag name must be unique.'),
    ]