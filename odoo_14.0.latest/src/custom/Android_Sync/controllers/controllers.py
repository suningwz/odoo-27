# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class AndroidSync(http.Controller):
    @http.route('/contacto', auth='public', website= True)
    def contacto_redirect(self):
        return request.redirect('/contactus')