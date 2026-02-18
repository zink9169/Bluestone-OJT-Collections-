from odoo import models, fields, api

class BssStudent(models.Model):
    _name = "bss.student"
    _description = "Student"

    name = fields.Char(required=True)
    student_number = fields.Char(readonly=True, copy=False)

    class_id = fields.Many2one("bss.class", string="Class")
    subject_ids = fields.Many2many("bss.subject")
    contact_id = fields.Many2one("res.partner", string="Contact Person")

    @api.model
    def create(self, vals):
        """
        Safely handle both single dict and list of dicts for creation.
        """
        # Wrap single dict into list for uniform processing
        single = False
        if isinstance(vals, dict):
            vals = [vals]
            single = True

        for v in vals:
            if not v.get("student_number"):
                v["student_number"] = self.env["ir.sequence"].next_by_code("bss.student")

        records = super(BssStudent, self).create(vals)
        return records[0] if single else records

    def write(self, vals):
        res = super().write(vals)
        if "name" in vals:
            for record in self:
                if record.contact_id:
                    record.contact_id.name = record.name
        return res

    @api.onchange("class_id")
    def _onchange_class_id(self):
        if self.class_id:
            self.subject_ids = [(6, 0, self.class_id.subject_ids.ids)]
