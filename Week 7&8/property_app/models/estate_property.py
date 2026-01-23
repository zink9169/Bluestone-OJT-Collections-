from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import timedelta


# --------------------------------------------------
# 1. Property Type
# --------------------------------------------------
class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "Property type name must be unique!",
        )
    ]


# --------------------------------------------------
# 2. Property Tag
# --------------------------------------------------
class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()


# --------------------------------------------------
# 3. Property
# --------------------------------------------------
class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive!",
        )
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False,
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type"
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag", string="Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    total_area = fields.Integer(
        compute="_compute_total_area", string="Total Area"
    )
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Price"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (
                record.living_area or 0
            ) + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 0.01):
                if float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    0.01,
                ) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% "
                        "of the expected price."
                    )

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(
                    "A canceled property cannot be set as sold."
                )
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(
                    "A sold property cannot be canceled."
                )
            record.state = "canceled"
        return True


# --------------------------------------------------
# 4. Property Offer
# --------------------------------------------------
class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = base_date + timedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.validity = (
                record.date_deadline - base_date
            ).days

    @api.model
    def create(self, vals):
        offer = super().create(vals)
        offer.property_id.state = "offer_received"
        return offer

    def action_accept(self):
        for record in self:
            property = record.property_id

            if any(
                o.status == "accepted"
                for o in property.offer_ids
            ):
                raise UserError(
                    "This property already has an accepted offer."
                )

            if record.price < property.expected_price * 0.9:
                raise UserError(
                    "You cannot accept an offer lower than 90% "
                    "of the expected price."
                )

            record.status = "accepted"
            property.buyer_id = record.partner_id
            property.selling_price = record.price
            property.state = "offer_accepted"

        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True


# --------------------------------------------------
# 5. Users Inheritance
# --------------------------------------------------
class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        domain=[("state", "in", ["new", "offer_received"])],
        string="Properties",
    )
