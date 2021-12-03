# -*- coding: utf-8 -*-

from odoo import models, fields, api

class examen_tecnico(models.Model):
     _name = 'examen_tecnico.examen_tecnico'
     _description = 'examen_tecnico.examen_tecnico'

     name = fields.Char()
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
         for record in self:
             record.value2 = float(record.value) / 100
