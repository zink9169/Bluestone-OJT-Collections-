from odoo import models, Command


class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Call parent method first
        result = super().action_sold()

        # Create invoice for each sold property
        for property in self:
            # Create invoice
            invoice = self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',  # Customer Invoice
                'journal_id': self.env['account.journal'].search([
                    ('type', '=', 'sale'),
                    ('company_id', '=', self.env.company.id)
                ], limit=1).id,
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission for property sale',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,  # 6% commission
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00,  # Fixed admin fee
                    }),
                ]
            })

            # Optional: Validate the invoice
            # invoice.action_post()

        return result