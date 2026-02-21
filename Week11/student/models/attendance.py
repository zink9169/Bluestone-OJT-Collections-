from odoo import models, fields, api
from datetime import datetime


class SchoolAttendance(models.Model):
    _name = 'school.attendance'
    _description = 'Attendance'

    name = fields.Char(string="Description")

    attendance_number = fields.Char(
        string="Attendance Number",
        readonly=True,
        copy=False,
        default='New'
    )

    date = fields.Date(string="Date", default=fields.Date.today)

    student_id = fields.Many2one('school.student', string="Student")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('attendance_number', 'New') == 'New':
                vals['attendance_number'] = self.env['ir.sequence'].next_by_code(
                    'school.attendance.sequence'
                ) or 'New'
        return super().create(vals_list)