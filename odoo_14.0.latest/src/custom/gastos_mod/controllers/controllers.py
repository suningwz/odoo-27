# -*- coding: utf-8 -*-
# from odoo import http


# class GastosMod(http.Controller):
#     @http.route('/gastos_mod/gastos_mod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gastos_mod/gastos_mod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gastos_mod.listing', {
#             'root': '/gastos_mod/gastos_mod',
#             'objects': http.request.env['gastos_mod.gastos_mod'].search([]),
#         })

#     @http.route('/gastos_mod/gastos_mod/objects/<model("gastos_mod.gastos_mod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gastos_mod.object', {
#             'object': obj
#         })
