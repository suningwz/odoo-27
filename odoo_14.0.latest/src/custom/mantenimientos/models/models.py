# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class mantenimientos(models.Model):
    _inherit = 'maintenance.request'

    fecha_inicio = fields.Date('Fecha de Inicio')
    fecha_liberacion = fields.Date('Fecha de liberacion')
    solicito = fields.Many2one('res.partner', domain="[('category_id', '=', 'Solicitante')]")
    cliente = fields.Many2one('res.partner', domain="[('category_id', '=', 'Cliente')]")
    tipo_unidad = fields.Selection([('n/a', 'N/A'), ('atm', 'ATM'), ('edf', 'EDF'), ('ofc', 'OFC')], 'Unidad')
    codigo = fields.Char('Codigo')
    nombre_cejero = fields.Char('Nombre')
    ciudad_cajero = fields.Char('Ciudad')
    codificador = fields.Selection([('p1', 'p1'), ('p2', 'p1')], 'codificador', default='p1')

    def formato_identificador(self):
        if not self.id:
            dato = "Nuevo"
        else:
            dato = self.id
        return dato

    @api.constrains('num_identificado')
    def asignacion_formato(self):
        if self.num_identificado == 'Nuevo':
            fecha = datetime.datetime.now()
            dato = f"MTTO-{fecha.year}{self.id}"
            print(dato)
            self.num_identificado = dato
            if self.name == 'Nuevo':
                self.name = dato
            else:
                numero = self.name
                if numero:
                    contact = self.env["maintenance.request"].search(
                        [("name", "=", self.name)]
                    )
                    if contact:
                        for c in contact:
                            if c.id != self.id:
                                raise Warning('El numero de solicitud ya existe, favor validar')
            self.user_id = self.maintenance_team_id.lider

    num_identificado = fields.Char('Identificacion interna', default=formato_identificador)


    @api.onchange('name')
    def asignar_name(self):
        if not self.name:
            self.name = self.num_identificado

    @api.onchange('fecha_inicio')
    def asignarfechas(self):
        self.schedule_date = self.fecha_inicio

    def buscar_cajeros(self):
        cajero = self.env["res.partner"].search(
            [("parent_id", "=", self.cliente.name), ("codigo", "=", self.codigo),
             ("tipo_unidad", "=", self.tipo_unidad)], limit=1
        )
        if not cajero:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context[
                'message'] = "No se encontro ningun elemento con esas especificaciones"
            return {
                'name': 'ADVERTENCIA',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_model': 'form',
                'res_model': 'sh.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
            }
        else:
            self.nombre_cejero = cajero.name
            self.ciudad_cajero = cajero.city

        self.codificador = 'p2'
