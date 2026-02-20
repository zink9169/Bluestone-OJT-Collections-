from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BssAttendance(models.Model):
    _name = "bss.attendance"
    _description = "Attendance"
    _rec_name = "attendance_number"

    # -------------------------------------------------
    # DATABASE LEVEL UNIQUE CONSTRAINT
    # -------------------------------------------------
    _sql_constraints = [
        (
            'unique_attendance_per_day',
            'unique(class_id, subject_id, student_id, date)',
            'Attendance already exists for this student, subject, class and date!'
        )
    ]

    # -------------------------------------------------
    # FIELDS
    # -------------------------------------------------
    attendance_number = fields.Char(
        string="Attendance Number",
        readonly=True,
        copy=False,
        default="New"
    )

    class_id = fields.Many2one("bss.class", required=True)
    subject_id = fields.Many2one("bss.subject", required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    student_id = fields.Many2one("bss.student", required=True)

    status = fields.Selection([
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused")
    ], default="present")

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            # Generate sequence
            if vals.get("attendance_number", "New") == "New":
                vals["attendance_number"] = self.env[
                    "ir.sequence"
                ].next_by_code("bss.attendance") or "New"

            self._validate_attendance(vals)

        return super().create(vals_list)

    # -------------------------------------------------
    # WRITE
    # -------------------------------------------------
    def write(self, vals):
        for rec in self:
            updated_vals = {
                'class_id': vals.get('class_id', rec.class_id.id),
                'subject_id': vals.get('subject_id', rec.subject_id.id),
                'student_id': vals.get('student_id', rec.student_id.id),
                'date': vals.get('date', rec.date),
            }
            self._validate_attendance(updated_vals, rec.id)

        return super().write(vals)

    # -------------------------------------------------
    # CENTRAL VALIDATION
    # -------------------------------------------------
    def _validate_attendance(self, vals, record_id=None):

        class_id = vals.get('class_id')
        subject_id = vals.get('subject_id')
        student_id = vals.get('student_id')
        attendance_date = vals.get('date')

        # -----------------------------
        # DATE VALIDATION (ONLY TODAY)
        # -----------------------------
        if attendance_date:
            attendance_date = fields.Date.to_date(attendance_date)
            today = fields.Date.context_today(self)

            if attendance_date != today:
                raise ValidationError(
                    "Attendance can only be taken for today!"
                )

        # -----------------------------
        # STUDENT BELONGS TO CLASS
        # -----------------------------
        if student_id and class_id:
            student = self.env['bss.student'].browse(student_id)
            if not student or student.class_id.id != class_id:
                raise ValidationError(
                    "Selected student does not belong to this class!"
                )

        if subject_id and class_id:
            class_obj = self.env['bss.class'].browse(class_id)
            if subject_id not in class_obj.subject_ids.ids:
                raise ValidationError(
                    "Selected subject does not belong to this class!"
                )