from odoo import models, fields, api

class BssAttendance(models.Model):
    _name = 'bss.attendance'
    _description = 'Attendance'

    attendance_number = fields.Char(
        string="Attendance Number", readonly=True, copy=False
    )
    student_id = fields.Many2one(
        'bss.student', string="Student", required=True
    )
    class_id = fields.Many2one(
        'bss.class', string="Class", required=True
    )
    date = fields.Date(string="Date", default=fields.Date.today)
    status = fields.Selection(
        [('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')],
        string="Status", default='present'
    )
    notes = fields.Text(string="Notes")

    @api.model
    def create(self, vals_list):
        # Handle batch creation safely
        for vals in vals_list:
            if not vals.get('attendance_number'):
                vals['attendance_number'] = self.env['ir.sequence'].next_by_code('bss.attendance') or 'ATD/0001'
        return super(BssAttendance, self).create(vals_list)