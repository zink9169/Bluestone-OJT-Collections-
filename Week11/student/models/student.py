from odoo import models, fields, api


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'

    name = fields.Char(required=True)
    user_id = fields.Many2one(
        'res.users',
        string='Related User',
        help="User linked to this student",
        ondelete='cascade'
    )
    student_number = fields.Char(
        readonly=True,
        copy=False,
        default='New'
    )

    class_id = fields.Many2one('school.class')
    subject_ids = fields.Many2many('school.subject')
    contact_person_id = fields.Many2one('res.partner')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('student_number', 'New') == 'New':
                vals['student_number'] = self.env['ir.sequence'].next_by_code(
                    'school.student.sequence'
                ) or 'New'
        return super().create(vals_list)

    # UPDATE CONTACT PERSON NAME WHEN STUDENT NAME CHANGES
    def write(self, vals):
        res = super(SchoolStudent, self).write(vals)

        if 'name' in vals:
            for rec in self:
                if rec.contact_person_id:
                    rec.contact_person_id.name = vals['name']

        return res

    # AUTO FILL SUBJECTS WHEN CLASS SELECTED
    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            self.subject_ids = [(6, 0, self.class_id.subject_ids.ids)]