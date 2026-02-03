from odoo import http
from odoo.http import request

class TodoController(http.Controller):

    @http.route('/todo', auth='user')
    def todo_page(self):
        return request.render('web.webclient_bootstrap')
