from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], default='pending', copy=False, readonly=True)

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
    )

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    # COMPUTE DEADLINE
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date).date()
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date).date()
                record.validity = (record.date_deadline - create_date).days

    # OVERRIDE CREATE
    @api.model
    def create(self, vals_list):
        # Ensure we always work with a list
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        offers = self.env['estate.property.offer']

        for vals in vals_list:
            property_rec = self.env['estate.property'].browse(vals.get('property_id'))

            # Check higher offer rule
            if property_rec.offer_ids:
                max_price = max(property_rec.offer_ids.mapped('price'))
                if vals.get('price', 0) <= max_price:
                    raise UserError(
                        "The offer must be higher than the existing offers."
                    )

            offer = super(EstatePropertyOffer, self).create(vals)
            offers |= offer

            # Update property state automatically if new
            if property_rec.state == 'new':
                property_rec.state = 'offer_received'

        return offers

    # ACTIONS
    def action_accept(self):
        for record in self:
            if record.status != 'pending':
                continue

            # Refuse all other offers
            other_offers = record.property_id.offer_ids.filtered(
                lambda o: o.id != record.id
            )
            other_offers.write({'status': 'refused'})

            # Accept this offer
            record.status = 'accepted'

            # Update property: selling price, buyer, and state to offer_accepted
            record.property_id.write({
                'selling_price': record.price,
                'buyer_id': record.partner_id,
                'state': 'offer_accepted',
            })

    def action_refuse(self):
        for record in self:
            if record.status == 'pending':
                record.status = 'refused'
