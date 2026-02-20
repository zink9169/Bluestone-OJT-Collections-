from odoo import models, fields, api
from datetime import datetime


class Attendance(models.Model):
    _name = 'bss.attendance'
    _description = 'Attendance'
    _order = 'date desc, id desc'
    _rec_name = 'attendance_number'

    attendance_number = fields.Char(string="Attendance Number", readonly=True, copy=False, index=True)
    student_id = fields.Many2one('bss.student', string="Student", required=True)
    date = fields.Date(string="Date", default=fields.Date.today, required=True)

    # Add status field with options
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ], string="Status", required=True, default='present')

    # Add class selection field (optional - can be used to filter students)
    class_id = fields.Many2one('bss.class', string="Class")

    # Add notes field
    notes = fields.Text(string="Notes")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('attendance_number'):
                now = datetime.now()
                year = now.strftime('%Y')
                month = now.strftime('%b').upper()
                seq = self.env['ir.sequence'].next_by_code('attendance.number.seq') or '0000'
                vals['attendance_number'] = f"ATD/{year}/{month}/{seq}"
        return super().create(vals_list)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.attendance_number} - {record.student_id.name} ({dict(record._fields['status'].selection).get(record.status)})"
            result.append((record.id, name))
        return result