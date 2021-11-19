# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class mantenimientos(models.Model):
    _inherit = 'maintenance.request'

    fecha_inicio = fields.Datetime('Fecha de Inicio')
    fecha_liberacion = fields.Date('Fecha de liberacion')
    solicito = fields.Many2one('res.partner', domain="[('category_id', '=', 'Solicitante')]")
    cliente = fields.Many2one('res.partner', domain="[('category_id', '=', 'Cliente')]")
    tipo_unidad = fields.Selection([('n/a','N/A'),('atm', 'ATM'), ('edf', 'EDF'), ('ofc', 'OFC')],'Unidad')
    codigo = fields.Char('Codigo cajero')
    nombre_cejero = fields.Char('Nombre')
    ciudad_cajero = fields.Char('Ciudad')


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

    @api.onchange('fecha_inicio')
    def asignarfechas(self):
        self.schedule_date = self.fecha_inicio

    def buscar_cajeros(self):
        self.nombre_cejero = 'Prueba'
        self.ciudad_cajero = 'Prueba'