from odoo import models, Command
from odoo.exceptions import UserError

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold(self):

        result = super().action_sold()
        for record in self:

            if not record.buyer_id:
                raise UserError("You must set a buyer before selling the property.")

            journal = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            if not journal:
                raise UserError("No Sales Journal found.")

            invoice = self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_origin': record.name,
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission for property sale (6%)',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            })

        return result
