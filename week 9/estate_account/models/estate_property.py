from odoo import models, Command
from odoo.exceptions import UserError

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("🔥 action_sold() CALLED")
        print("➡ Records:", self)

        result = super().action_sold()
        print("✅ super().action_sold() DONE")

        for record in self:
            print("🏠 Processing property:", record.name)
            print("   Buyer:", record.buyer_id)
            print("   Selling Price:", record.selling_price)

            if not record.buyer_id:
                print("❌ No buyer set")
                raise UserError("You must set a buyer before selling the property.")

            if not record.selling_price:
                print("❌ No selling price")
                raise UserError("You must set a selling price before selling the property.")

            journal = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)

            print("📘 Sales Journal:", journal)

            if not journal:
                print("❌ No Sales Journal found")
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

            print("🧾 Invoice CREATED → ID:", invoice.id)

        print("🏁 action_sold() FINISHED")
        return result
