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

    inventario = fields.One2many('stock.quant','opuesto')

    transferencias = fields.One2many('stock.picking', 'opuesto')
    movimiento_inventario = fields.One2many('stock.inventory', 'opuesto')

    ajustes_inventario = fields.Many2one

    ejecucion_tecnica = fields.Selection(
        [("r1", "Se puede ejecutar"), ("r2", "No se puede ejecutar")],
        string="¿El servicio se puede realizar inmediatamente?"
    )
    Motivos_no = fields.Selection(
        [('f1', 'Funcionario no puede atender al tecnico'),
         ('f2', 'Funcionario no se encuentra en la sucursal'),
         ('f3', 'Horario restringido'),
         ('f4', 'No hubo correo de permiso de ingreso'),
         ('f5', 'No se puede realizar inmediatamente'),
         ('f6', 'Operador central desconoce servio a Ejecutar'),
         ('f7', 'Operador central no contesta llamada'),
         ('f8', 'Operador global no contesta llamada'),
         ('f9', 'Otro proveedor no hace presencia en el sitio'),
         ('f10', 'Panel de alarma dentro de la scucursal'),
         ('f11', 'Proveedor no apertura otros cajeros'),
         ('f12', 'Proveedor no lleva llaves'),
         ('f13', 'Se requiere curso de seguridad industrial'),
         ('f14', 'Sin permiso de ingreso para otro proveedor'),
         ('f15', 'Sucursal con alto flujo de usuarios'),
         ('f16', 'Tecnico no alcanza a llegar'),
         ('f17', 'Transportadora no hace presencia en el sitio')],
        string='Motivo por el cual no se puede realizar')

    coordenadas = fields.Char(string='coordenadas')
    @api.onchange('ejecucion_tecnica')
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
            if not self.date_end:
                self.date_end = datetime.now()

    @api.onchange('person_id')
    def default_inventario(self):
        warehouse_ids = self.env["stock.warehouse"].search(
            [("name", "=", self.person_id.name)], limit=1
        )
        elements = self.env["stock.quant"].search(
            [("location_id", "=", f"{warehouse_ids.code}/Existencias")]
        )
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

class odoocontroler(http.Controller):
    @http.route(['/ajax-geolocalizacion'],type='json', auth='public',methods=['POST'])
    def geolocalizacion(self, **kw):
        geo = Nominatim(user_agent="odoo_localizacion")
        cor = f"{kw['latitude']}, {kw['longitud']}"
        loc = geo.reverse(cor)
        print(loc)
        warehouse_ids = request.env["fsm.order"].search(
            [("name", "=", kw['name'])], limit=1
        )
        warehouse_ids.coordenadas = loc
        p = {
            "Estatus" : "0k"
        }
        return p





