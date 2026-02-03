from odoo import http
from odoo.http import request

class OwlCounterController(http.Controller):

    @http.route('/owl/counter', auth='user')
    def open_counter(self):
        return request.render('web.webclient_bootstrap')
