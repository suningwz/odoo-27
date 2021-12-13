# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Reports(models.Model):
     _name = 'reports'
     _inherit = ['fsm.order']
     _description = "reports model"
     
     name = fields.Char(string="Nombre del Reporte", required=True)
     template_id = fields.Char(string="Plantilla", required=True)
     person_id = fields.Char(string="Asignado a : ", required=True)

