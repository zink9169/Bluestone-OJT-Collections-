from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'bss.student'
    _description = 'Student'
    _order = 'student_number'

    # Remove tracking parameter if mail module is not properly installed
    user_id = fields.Many2one('res.users', string="Related User")
    name = fields.Char(string="Name", required=True)
    student_number = fields.Char(string="Student Number", readonly=True, copy=False, default='New')
    contact_person_name = fields.Char(string="Contact Person Name")

    class_ids = fields.Many2many('bss.class', string="Classes")
    subject_ids = fields.Many2many('bss.subject', string="Subjects")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('student_number', 'New') == 'New':
                vals['student_number'] = self.env['ir.sequence'].next_by_code('student.number.seq')
        return super().create(vals_list)

    @api.onchange('name')
    def _onchange_name_sync_contact(self):
        if self.name:
            self.contact_person_name = self.name

    @api.onchange('class_ids')
    def _onchange_class_ids_fill_subjects(self):
        """When classes change, update subjects based on selected classes"""
        if self.class_ids:
            # Get all subjects from all selected classes
            all_subjects = self.class_ids.mapped('subject_ids')

            if all_subjects:
                if self.subject_ids:
                    combined_subjects = self.subject_ids | all_subjects
                    self.subject_ids = [(6, 0, combined_subjects.ids)]
                else:
                    self.subject_ids = [(6, 0, all_subjects.ids)]

    @api.constrains('user_id')
    def _check_unique_user(self):
        for record in self:
            if record.user_id:
                existing = self.search([
                    ('user_id', '=', record.user_id.id),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(
                        f"User {record.user_id.name} is already linked to another student!"
                    )

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.student_number}] {record.name}" if record.student_number else record.name
            result.append((record.id, name))
        return result