from odoo import fields, models


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'seller_id',  # ← This matches your estate.py field name
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received', 'offer_accepted'])]
    )