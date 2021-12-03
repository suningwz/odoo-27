# -*- coding: utf-8 -*-
# from odoo import http


# class ExamenTecnico(http.Controller):
#     @http.route('/examen_tecnico/examen_tecnico/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/examen_tecnico/examen_tecnico/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('examen_tecnico.listing', {
#             'root': '/examen_tecnico/examen_tecnico',
#             'objects': http.request.env['examen_tecnico.examen_tecnico'].search([]),
#         })

#     @http.route('/examen_tecnico/examen_tecnico/objects/<model("examen_tecnico.examen_tecnico"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('examen_tecnico.object', {
#             'object': obj
#         })
