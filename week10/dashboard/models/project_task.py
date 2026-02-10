from odoo import models, api, fields
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_urgent = fields.Boolean(string="Is Urgent", default=False)

    @api.model
    def get_dashboard_data(self):
        today = fields.Date.today()
        next_week = today + timedelta(days=7)

        def get_section_data(title, color, domain):
            task_model = self.with_context(active_test=False)
            search_domain = ['|', ('active', '=', True), ('active', '=', False)] + domain

            count = task_model.search_count(search_domain)
            tasks = task_model.search_read(
                search_domain,
                ['name', 'project_id', 'date_deadline', 'state', 'create_date'],
                limit=5,
                order='create_date desc'
            )

            return {
                'title': title,
                'color': color,
                'count': count,
                'tasks': tasks,
                # ✅ VERY IMPORTANT (FIX)
                'domain': domain,
            }

        return {
            'dates': {
                'today': fields.Date.to_string(today),
                'next_week': fields.Date.to_string(next_week),
            },
            'sections': {
                'new': get_section_data(
                    'New Request Tasks',
                    '#FFB300',
                    [('state', 'in', ['02_changes_requested'])]
                ),
                'progress': get_section_data(
                    'In Progress',
                    '#2E7D32',
                    [('state', '=', '01_in_progress')]
                ),
                'done': get_section_data(
                    'Done',
                    '#6c757d',
                    [('state', '=', '1_done')]
                ),
                'due_soon': get_section_data(
                    'Due Soon',
                    '#00bcd4',
                    [
                        ('date_deadline', '>=', today),
                        ('date_deadline', '<=', next_week),
                        ('state', 'not in', ['1_done', '1_canceled'])
                    ]
                ),
                'overdue': get_section_data(
                    'Overdue',
                    '#f44336',
                    [
                        ('date_deadline', '<', today),
                        ('state', 'not in', ['1_done', '1_canceled'])
                    ]
                ),
                'urgent': get_section_data(
                    'Urgent Request',
                    '#e91e63',
                    [('is_urgent', '=', True), ('state', '!=', '1_done')]
                ),
            }
        }
