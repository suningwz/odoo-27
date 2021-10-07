import requests
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models, http
from odoo.http import request
from datetime import datetime
import json
from xlsxwriter import app
from geopy.geocoders import Nominatim
import time
import math
import urllib.request


class almacen_tecnico(models.Model):
    _inherit = 'fsm.order'

    inventario = fields.One2many('stock.quant', 'opuesto')
    firma = fields.Binary(
        string='En el siguiente recuandro ingrese la firma.')
    q_firma = fields.Char('Nombre de quien firma')
    cc_q_firma = fields.Integer('Documento de la persona que firma')
    transferencias = fields.One2many('stock.picking', 'opuesto')
    movimiento_inventario = fields.One2many('stock.inventory', 'opuesto')

    ajustes_inventario = fields.Many2one

    ejecucion_tecnica = fields.Selection(
        [("r1", "Se puede ejecutar"), ("r2", "No se puede ejecutar")],
        string="¿El servicio se puede realizar inmediatamente?"
    )
    Motivos_no = fields.Selection(
        [('f1', 'No hay permiso de labores'),
         ('f2', 'No hay permiso de ingreso'),
         ('f3', 'Horario restringido'),
         ('f4', 'Proveedor de la maquina no hace presencia'),
         ('f5', 'Proveedor de la maquina llego tarde'),
         ('f6', 'Tdv llega tarde'),
         ('f7', 'Tecnico no alcanza a llegar'),
         ('f8', 'No hay acceso a punto de corriente'),
         ('f9', 'Cajero ya intervenido'),
         ('f10', 'Labores son en horario nocturno'),
         ('f11', 'Transportadora no hace presencia en el sitio')],
        string='Motivo por el cual no se puede realizar')

    coordenadas = fields.Char(string='Coordenadas')
    datos_personales = fields.Boolean(default=False)
    correo_representante = fields.Char()

    @api.onchange('project_task_id')
    def state_asignacion(self):
        id_state = int(self.project_task_id.stage_id)
        if id_state == 2:
            self.project_task_id.stage_id = 3

    def aceptacion_datos(self):
        self.datos_personales = True

    @api.onchange('ejecucion_tecnica')
    def time_initial(self):
        if self.ejecucion_tecnica == 'r1':
            self.date_start = datetime.now()

    @api.onchange('Motivos_no')
    def default_time(self):
        if self.ejecucion_tecnica == 'r2':
            if not self.date_start:
                self.date_start = datetime.now()
                self.date_end = datetime.now()
        elif self.ejecucion_tecnica == 'r1':
            if not self.date_start:
                self.date_start = datetime.now()

    def time_end(self):
        if self.ejecucion_tecnica == 'r1':
            self.date_end = datetime.now()
            variable = self.env["product.template"].search(
                [("name", "=", "SUMINISTRO E INSTALACION DE KIT TRAMPA DE CAJEROS NCR S23")], limit=1)
            if not variable:
                print("error no se encontro nada")
            else:
                self.contractor_cost_ids = [
                    (0, 0, {'product_id': variable.id, 'quantity': 1, 'price_unit': variable.standard_price})]
        id_state = int(self.project_task_id.stage_id)
        if id_state == 4:
            self.project_task_id.stage_id = 5



    @api.onchange('person_id')
    def default_inventario(self):
        warehouse_ids = self.env["stock.warehouse"].search(
            [("name", "=", self.person_id.name)], limit=1
        )
        elements = self.env["stock.quant"].search(
            [("location_id", "=", f"{warehouse_ids.code}/Existencias")]
        )
        if not self.person_id:
            print(' ')
        else:
            id_state = int(self.project_task_id.stage_id)
            print(id_state)
            if id_state == 3:
                self.project_task_id.stage_id = 4
        if not elements:
            print('vacio')
        else:
            x = str(elements).split('(')
            y = len(x)
            print(y)
            x = x[1].split(')')
            x = x[0].split(',')
            y = len(x)
            print(y)
            if int(y) < 1:
                print(x)
            else:
                for j in range(y):
                    print(x[j])
                    if not x[j]:
                        print('vacio')
                    else:
                        resultado = x[j]
                        resultado = int(resultado)
                        self.inventario = [(4, resultado)]

    def default2(self):
        print('ingreso')
        self.inventario = [(5,)]
        self.default_inventario()


class opuesto_tecnico(models.Model):
    _inherit = 'stock.quant'

    opuesto = fields.Many2one('fsm.order', string="", readonly="True")


class opuesto_tecnico(models.Model):
    _inherit = 'stock.picking'
    opuesto = fields.Many2one('fsm.order', string="", readonly="True")


class opuesto_tecnico(models.Model):
    _inherit = 'stock.inventory'
    opuesto = fields.Many2one('fsm.order', string="", readonly="True")


# esto es un controlador que se usar para recibir los paremtros mediante un archivo JSON del front enviado por JS para poder calcular la geolocalizacion
class odoocontroler(http.Controller):
    @http.route(['/ajax-geolocalizacion'], type='json', auth='public', methods=['POST'])
    def geolocalizacion(self, **kw):
        geo = Nominatim(user_agent="odoo_localizacion")
        # cor = f"{kw['latitude']}, {kw['longitud']}"
        url = f"https://www.google.com/maps/place/{kw['latitude']}, {kw['longitud']}"
        # print(cor)
        # loc = geo.reverse(cor)
        # print(loc)
        warehouse_ids = request.env["fsm.order"].search(
            [("name", "=", kw['name'])], limit=1
        )
        warehouse_ids.coordenadas = url
        p = {
            "Estatus": "0k"
        }
        return p


class product_template(models.Model):
    _inherit = 'product.template'
    marca = fields.Char(string="Marca")
