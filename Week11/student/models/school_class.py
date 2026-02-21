from odoo import models, fields


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name = fields.Char(string="Class Name")

    subject_ids = fields.Many2many(
        'school.subject',
        string="Subjects"
    )


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'

    name = fields.Char(string="Subject Name")