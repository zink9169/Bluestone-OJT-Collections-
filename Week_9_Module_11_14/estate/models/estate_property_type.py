from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    
    name = fields.Char(required=True)

    # === SQL CONSTRAINTS ===
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'Property type name must be unique.'),
    ]