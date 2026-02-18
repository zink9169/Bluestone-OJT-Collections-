from odoo import models, fields, api


class BssAttendance(models.Model):
    _name = "bss.attendance"
    _description = "Attendance"
    _rec_name = "attendance_number"

    name = fields.Char(string="Description")

    attendance_number = fields.Char(
        string="Attendance Number",
        readonly=True,
        copy=False,
        default="New"
    )

    student_id = fields.Many2one(
        "bss.student",
        string="Student",
        required=True,
        ondelete="cascade"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Auto-generate sequence for attendance_number.
        Works for single and multiple record creation.
        """

        for vals in vals_list:
            if vals.get("attendance_number", "New") == "New":
                vals["attendance_number"] = self.env[
                    "ir.sequence"
                ].next_by_code("bss.attendance") or "New"

        return super().create(vals_list)
