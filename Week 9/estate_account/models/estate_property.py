from odoo import models, Command

class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        res = super(Property, self).action_sold()

        for record in self:
            commission_price = record.selling_price * 0.06
            administrative_fees = 100.00

            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Commission for {record.name}",
                        "quantity": 1.0,
                        "price_unit": commission_price,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1.0,
                        "price_unit": administrative_fees,
                    }),
                ],
            })
        return res