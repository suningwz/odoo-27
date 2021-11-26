# -*- coding: utf-8 -*-
from odoo import models, fields, api
import time
import pytz
from datetime import datetime
from datetime import timedelta
from calendar import day_name


class mantenimientos(models.Model):
    _inherit = 'maintenance.request'

    fecha_inicio = fields.Date('Fecha de Inicio')
    fecha_fin = fields.Date('Fecha fin')
    solicito = fields.Many2one('res.partner', domain="[('category_id', '=', 'Solicitante')]")
    cliente = fields.Many2one('res.partner', domain="[('category_id', '=', 'Cliente')]")
    tipo_unidad = fields.Selection([('n/a', 'N/A'), ('atm', 'ATM'), ('edf', 'EDF'), ('ofc', 'OFC')], 'Unidad')
    codigo = fields.Char('Codigo')
    nombre_cejero = fields.Char('Nombre')
    ciudad_cajero = fields.Char('Ciudad')
    codificador = fields.Selection([('p1', 'p1'), ('p2', 'p1')], 'codificador', default='p1')
    ordenes_fsm = fields.One2many('fsm.order', 'mantenimientos')
    fecha_h_liberacion = fields.Datetime('F/H de liberacion')

    @api.onchange('fecha_h_liberacion')
    def hora_liberacion_campos(self):
        self.request_date = self.fecha_h_liberacion

    def formato_identificador(self):
        if not self.id:
            dato = "Nuevo"
        else:
            dato = self.id
        return dato

    @api.constrains('num_identificado')
    def asignacion_formato(self):
        if self.num_identificado == 'Nuevo':
            fecha = datetime.now()
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
        if not self.request_date:
            print("No se puede")
        else:
            tomorrow = datetime.now()
            dia = self.request_date
            cont = 1
            for x in range(5):
                cont = cont + 1
                tomorrow = dia + timedelta(cont)
                wek = day_name[tomorrow.weekday()]
                d1 = tomorrow.strftime("%d/%m")
                if wek == "Saturday":
                    cont = cont + 1
                elif wek == "Sunday":
                    cont = cont + 1
                elif d1 == "01/01":
                    cont = cont + 1
                elif d1 == "11/01":
                    cont = cont + 1
                elif d1 == "22/03":
                    cont = cont + 1
                elif d1 == "01/04":
                    cont = cont + 1
                elif d1 == "02/04":
                    cont = cont + 1
                elif d1 == "01/05":
                    cont = cont + 1
                elif d1 == "17/05":
                    cont = cont + 1
                elif d1 == "07/06":
                    cont = cont + 1
                elif d1 == "14/06":
                    cont = cont + 1
                elif d1 == "05/07":
                    cont = cont + 1
                elif d1 == "20/07":
                    cont = cont + 1
                elif d1 == "07/08":
                    cont = cont + 1
                elif d1 == "16/08":
                    cont = cont + 1
                elif d1 == "18/10":
                    cont = cont + 1
                elif d1 == "01/11":
                    cont = cont + 1
                elif d1 == "15/11":
                    cont = cont + 1
                elif d1 == "08/12":
                    cont = cont + 1
                elif d1 == "25/12":
                    cont = cont + 1
            print(self.maintenance_team_id.lider.id)
            data = {
                'res_id': self.id,
                'user_id': self.maintenance_team_id.lider.id,
                'res_model_id': 444,
                'summary': 'Nueva solicitud',
                'activity_type_id': 4,
                'date_deadline': tomorrow
            }
            creacion_tarea = self.env['mail.activity'].create(data)

    def crear_fsm(self):
        action = self.env.ref("fieldservice.action_fsm_operation_order")
        result = action.read()[0]
        # parametros que se le pasan por contexto

        result["context"] = {
            "default_project_id": self.id,
            "default_mantenimientos": self.id,
            "cajero": self.nombre_cejero,
        }
        res = self.env.ref("fieldservice.fsm_order_form", False)
        result["views"] = [(res and res.id or False, "form")]
        return result


class conection_fsm(models.Model):
    _inherit = 'fsm.order'

    mantenimientos = fields.Many2one('maintenance.request')
