from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero  # ← ADD THIS IMPORT
from datetime import datetime, timedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"  # Show newest properties first

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: datetime.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True, copy=False, tracking=True)

    # Many2one relationships
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    # Many2many relationship
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # One2many relationship
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(
        string="Total Area",
        compute="_compute_total_area",
        store=True,
        help="Sum of living area and garden area"
    )

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True,
        help="Highest offer price received"
    )

    # === DYNAMIC BUTTON FIELDS ===
    sold_button_text = fields.Char(
        compute="_compute_button_text",
        string="Sold Button Text",
        store=False  # Don't store, compute on the fly
    )
    sold_button_class = fields.Char(
        compute="_compute_button_text",
        string="Sold Button Class",
        store=False
    )
    cancel_button_text = fields.Char(
        compute="_compute_button_text",
        string="Cancel Button Text",
        store=False
    )
    cancel_button_class = fields.Char(
        compute="_compute_button_text",
        string="Cancel Button Class",
        store=False
    )

    # === SQL CONSTRAINTS ===
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.'),
    ]

    # === COMPUTE METHODS ===
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                valid_offers = record.offer_ids.filtered(lambda o: o.status != 'refused')
                if valid_offers:
                    record.best_price = max(valid_offers.mapped('price'))
                else:
                    record.best_price = 0.0
            else:
                record.best_price = 0.0

    @api.depends('state')
    def _compute_button_text(self):
        """Compute button text and classes based on state"""
        for record in self:
            # Sold button
            if record.state == 'sold':
                record.sold_button_text = "✓ Sold"
                record.sold_button_class = "btn-success"
            else:
                record.sold_button_text = "Set as Sold"
                record.sold_button_class = "btn-primary"

            # Cancel button
            if record.state == 'canceled':
                record.cancel_button_text = "✗ Canceled"
                record.cancel_button_class = "btn-secondary"
            else:
                record.cancel_button_text = "Cancel"
                record.cancel_button_class = "btn-danger"

    # === PYTHON CONSTRAINTS ===
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_90_percent(self):  # ← RENAMED to avoid conflict
        """Check selling price is not lower than 90% of expected price"""
        for record in self:
            # Skip check if selling price is 0 (not set yet)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            # Calculate 90% of expected price
            min_price = record.expected_price * 0.9

            # Compare selling price with 90% of expected price
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    f"The selling price cannot be lower than 90% of the expected price. "
                    f"Minimum selling price: {min_price:.2f}"
                )

    # === ONCHANGE METHOD ===
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # === ACTION METHODS ===
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            if record.state == 'sold':
                raise UserError("Property is already sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            if record.state == 'canceled':
                raise UserError("Property is already canceled.")
            record.state = 'canceled'
        return True

    # === ADDITIONAL METHOD FOR OFFER STATE MANAGEMENT ===
    @api.depends('offer_ids.status')
    def _compute_offer_state(self):
        """Update property state based on offers"""
        for prop in self:
            if prop.state in ['sold', 'canceled']:
                continue
            if prop.offer_ids:
                if any(offer.status == 'accepted' for offer in prop.offer_ids):
                    prop.state = 'offer_accepted'
                else:
                    prop.state = 'offer_received'
            else:
                prop.state = 'new'

    # Override write to update state when offers change
    def write(self, vals):
        result = super().write(vals)
        if 'offer_ids' in vals:
            self._compute_offer_state()
        return result