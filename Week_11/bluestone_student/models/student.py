from odoo import models, fields, api


class BssStudent(models.Model):
    _name = "bss.student"
    _description = "Student"

    name = fields.Char(
        string="Student Name",
        required=True,
    )

    student_number = fields.Char(
        string="Student Number",
        readonly=True,
        copy=False
    )

    father_name = fields.Char(string="Father's Name", required=True)
    location = fields.Char(string="Location", required=True)

    contact_person = fields.Char(
        string="Contact Person",
        required=True
    )

    user_id = fields.Many2one(
        "res.users",
        string="User Account",
        required=True
    )

    email = fields.Char(
        string="Email",
        related="user_id.login",
        store=True,
        readonly=True
    )

    phone = fields.Char(
        string="Phone",
        related="user_id.partner_id.phone",
        store=True,
        readonly=True
    )

    class_id = fields.Many2one(
        "bss.class",
        string="Class",
        required=True
    )

    subject_ids = fields.Many2many(
        "bss.subject",
        string="Subjects",
        required=True
    )

    subject_attendance_ids = fields.One2many(
        "bss.attendance",
        "student_id",
        string="Attendance Records"
    )

    attendance_percentage = fields.Text(
        string="Attendance % by Subject",
        compute="_compute_attendance_percentage",
        store=True
    )

    _sql_constraints = [
        ("unique_user", "unique(user_id)", "This user is already linked to another student!")
    ]

    # =========================
    # CREATE
    # =========================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Auto-fill name from user
            if vals.get("user_id") and not vals.get("name"):
                user = self.env["res.users"].browse(vals["user_id"])
                vals["name"] = user.name

            # Auto-fill contact from name
            if vals.get("name") and not vals.get("contact_person"):
                vals["contact_person"] = vals["name"]

            # Generate student number
            if not vals.get("student_number"):
                vals["student_number"] = (
                    self.env["ir.sequence"].next_by_code("bss.student") or "NEW"
                )

        return super().create(vals_list)

    # =========================
    # ONCHANGE
    # =========================
    @api.onchange("user_id")
    def _onchange_user_id(self):
        if self.user_id:
            self.name = self.user_id.name

            # Only set contact if empty (do not overwrite manual edit)
            if not self.contact_person:
                self.contact_person = self.user_id.name

    @api.onchange("name")
    def _onchange_name_set_contact(self):
        if self.name and not self.contact_person:
            self.contact_person = self.name

    @api.onchange("class_id")
    def _onchange_class_id(self):
        if self.class_id:
            self.subject_ids = [(6, 0, self.class_id.subject_ids.ids)]

    # =========================
    # COMPUTE ATTENDANCE
    # =========================
    @api.depends(
        "subject_ids",
        "subject_attendance_ids.status",
        "subject_ids.total_sessions",
    )
    def _compute_attendance_percentage(self):
        for student in self:
            if not student.subject_ids:
                student.attendance_percentage = "No subjects assigned."
                continue

            lines = []

            for subject in student.subject_ids:
                total = subject.total_sessions or 0

                if total > 0:
                    attended = self.env["bss.attendance"].search_count([
                        ("student_id", "=", student.id),
                        ("subject_id", "=", subject.id),
                        ("status", "=", "present"),
                    ])

                    percent = (attended / total) * 100
                    lines.append(f"{subject.name}: {percent:.0f}%")
                else:
                    lines.append(f"{subject.name}: 0%")

            student.attendance_percentage = "\n".join(lines)