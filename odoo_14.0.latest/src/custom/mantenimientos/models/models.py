# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class mantenimientos(models.Model):
    _inherit = 'maintenance.request'

    def formato_identificador(self):
        if not self.id:
            dato = "Nuevo"
        else:
            dato = self.id
        return dato


    @api.constrains('num_identificado')
    def asignacion_formato(self):
        if self.num_identificado=='Nuevo':
            print("ingresa")
            fecha = datetime.datetime.now()
            dato = f"MTTO-{fecha.year}{self.id}"
            print(dato)
            self.num_identificado = dato


    num_identificado = fields.Char('Identificacion interna', default= formato_identificador)

    
