from odoo import models, fields, api

class BssStudent(models.Model):
    _name = 'bss.student'
    _description = 'Student'

    name = fields.Char(string="Student Name", required=True)
    student_number = fields.Char(string="Student Number", readonly=True, copy=False)
    contact_person_id = fields.Many2one('res.partner', string="Contact Person")
    class_id = fields.Many2one('bss.class', string="Class")
    subject_ids = fields.Many2many('bss.subject', string="Subjects")
    user_id = fields.Many2one('res.users', string="Related User")

    @api.model
    def create(self, vals_list):
        # Ensure student_number is generated for each record
        for vals in vals_list:
            if not vals.get('student_number'):
                vals['student_number'] = self.env['ir.sequence'].next_by_code('bss.student') or 'STD/0001'
        students = super(BssStudent, self).create(vals_list)
        
        # Update contact person names
        for student in students:
            if student.contact_person_id:
                student.contact_person_id.name = student.name
        return students

    def write(self, vals):
        res = super(BssStudent, self).write(vals)
        if 'name' in vals:
            for student in self:
                if student.contact_person_id:
                    student.contact_person_id.name = student.name
        return res

    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            self.subject_ids = [(6, 0, self.class_id.subject_ids.ids)]