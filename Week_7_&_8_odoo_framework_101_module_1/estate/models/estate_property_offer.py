from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc, id desc"  # highest first, stable order

    # === FIELDS ===
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
        default=False,
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    # === SQL CONSTRAINTS ===
    _sql_constraints = [
        ("check_price_positive", "CHECK(price > 0)", "The offer price must be strictly positive."),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = (offer.create_date + timedelta(days=offer.validity)).date()
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
                continue

            # create_date can be False on new/unsaved records (onchange)
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

    # === ACTIONS ===
    def action_accept(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("This offer is already accepted.")
            if offer.status == "refused":
                raise UserError("Cannot accept a refused offer.")

            if offer.property_id.state == "sold":
                raise UserError("Cannot accept offer on a sold property.")
            if offer.property_id.state in ("cancelled", "canceled"):
                raise UserError("Cannot accept offer on a canceled property.")

            other_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.id != offer.id and o.status != "refused"
            )
            if other_offers:
                other_offers.write({"status": "refused"})

            offer.write({"status": "accepted"})

            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer_id": offer.partner_id.id,
                    "state": "offer_accepted",
                }
            )
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == "refused":
                raise UserError("This offer is already refused.")
            if offer.status == "accepted":
                raise UserError("Cannot refuse an accepted offer.")
            offer.write({"status": "refused"})
        return True
