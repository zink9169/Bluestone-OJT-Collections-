from odoo import models, fields, api

class ResGroupsDebug(models.Model):
    _inherit = 'res.groups'

    @api.model
    def get_fields(self):
        fields_list = self.fields_get()
        print("Available fields in res.groups:", list(fields_list.keys()))
        return True