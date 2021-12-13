# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class android__sync(models.Model):
#     _name = 'android__sync.android__sync'
#     _description = 'android__sync.android__sync'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
