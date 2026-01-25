from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta, date


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc, id desc"  # highest first, stable order

    # === FIELDS ===
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        string="Status",
        copy=False,
        default="pending",  # Default is now pending
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
                # Ensure we're working with date object
                create_date = fields.Date.to_date(offer.create_date)
                offer.date_deadline = create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
                continue

            # create_date can be False on new/unsaved records (onchange)
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

    # === CRON METHOD FOR EXPIRED OFFERS ===
    @api.model
    def _cron_check_expired_offers(self):
        """Automatically reject offers whose deadline has passed"""
        today = date.today()
        expired_offers = self.search([
            ('status', '=', 'pending'),
            ('date_deadline', '<', today)
        ])

        if expired_offers:
            expired_offers.write({'status': 'refused'})
            # In Odoo 19, we don't need manual commit for cron jobs

    # === ONCHANGE FOR VALIDITY ===
    @api.onchange('validity')
    def _onchange_validity(self):
        if self.validity:
            base_date = self.create_date.date() if self.create_date else fields.Date.today()
            self.date_deadline = base_date + timedelta(days=self.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        if self.date_deadline and self.create_date:
            base_date = self.create_date.date() if self.create_date else fields.Date.today()
            self.validity = (self.date_deadline - base_date).days

    # === ACTIONS ===
    def action_accept(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("This offer is already accepted.")
            if offer.status == "refused":
                raise UserError("Cannot accept a refused offer.")

            if offer.property_id.state == "sold":
                raise UserError("Cannot accept offer on a sold property.")
            if offer.property_id.state == "canceled":
                raise UserError("Cannot accept offer on a canceled property.")

            # Check if offer is expired
            if offer.date_deadline and offer.date_deadline < date.today():
                raise UserError("Cannot accept an expired offer.")

            # Reject all other offers on the same property
            other_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.id != offer.id and o.status in ['pending', 'accepted']
            )
            if other_offers:
                other_offers.write({"status": "refused"})

            # Accept current offer
            offer.write({"status": "accepted"})

            # Update property
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

            # If this was the only accepted offer, reset property state
            if offer.property_id.state == 'offer_accepted' and not offer.property_id.offer_ids.filtered(
                    lambda o: o.status == 'accepted'):
                offer.property_id.write({
                    'selling_price': 0,
                    'buyer_id': False,
                    'state': 'offer_received' if offer.property_id.offer_ids else 'new'
                })
        return True