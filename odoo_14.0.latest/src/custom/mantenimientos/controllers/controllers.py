# -*- coding: utf-8 -*-
# from odoo import http


# class Mantenimientos(http.Controller):
#     @http.route('/mantenimientos/mantenimientos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mantenimientos/mantenimientos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mantenimientos.listing', {
#             'root': '/mantenimientos/mantenimientos',
#             'objects': http.request.env['mantenimientos.mantenimientos'].search([]),
#         })

#     @http.route('/mantenimientos/mantenimientos/objects/<model("mantenimientos.mantenimientos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mantenimientos.object', {
#             'object': obj
#         })
