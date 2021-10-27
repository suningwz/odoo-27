import requests
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models, http
from odoo import SUPERUSER_ID
from odoo.http import request
from datetime import datetime
import json
from xlsxwriter import app
from geopy.geocoders import Nominatim
from odoo.exceptions import ValidationError
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

    conteo_inventario = fields.One2many('stock.quant', 'opuestofms')

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
            if not self.date_start:
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
            if not self.date_end:
                self.date_end = datetime.now()
                cliente = str( self.date_start - self.scheduled_date_start)
                entrega = str(self.date_end - self.scheduled_date_end)
                cliente = cliente.split('.')
                cliente = cliente[0]
                entrega = entrega.split('.')
                entrega = entrega[0]
                self.duration_cliente = cliente 
                self.duracion_entrega = entrega
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
    _inherit = 'stock.picking'
    opuesto = fields.Many2one('fsm.order', string="", readonly="True")
    nuevo_almacen = fields.Many2one('stock.location', string="Nuevo despacho")

    estado_kanban = fields.Many2one(
        'estado.transferencias',
        string='Estado del almacen', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict',
        default=1,)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # retrieve team_id from the context and write the domain
        # - ('id', 'in', stages.ids): add columns that should be present
        # - OR ('fold', '=', False): add default columns that are not folded
        # - OR ('team_ids', '=', team_id), ('fold', '=', False) if team_id: add team columns that are not folded
        team_id = self._context.get('default_team_id')
        if team_id:
            search_domain = ['|', ('id', 'in', stages.ids), '|', ('team_id', '=', False), ('team_id', '=', team_id)]
        else:
            search_domain = ['|', ('id', 'in', stages.ids), ('team_id', '=', False)]

        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def despacho_nuevo(self):
        self.location_id = self.nuevo_almacen

    def Notificacion_almacen(self):
        name_location = f"{self.location_id.location_id.name}/{self.location_id.name}"
        warehouse_ids = self.env["stock.warehouse"].search(
            [("lot_stock_id", "=", name_location)], limit=1
        ).partner_id.name
        personal = self.env["hr.employee"].search(
            [("name", "=", warehouse_ids)], limit=1
        )
        personal.user_id.notify_success(f'Nueva solicitud de elementos')


class opuesto_tecnico(models.Model):
    _inherit = 'stock.inventory'
    opuesto = fields.Many2one('fsm.order', string="", readonly="True")


class opuesto_conteo(models.Model):
    _inherit = 'stock.quant'
    opuesto = fields.Many2one('fsm.order', string="", readonly="True")
    opuestofms = fields.Many2one('fsm.order', string="", readonly="True")
    elementos_usados = fields.Float(string='Elmentos usados')

    @api.onchange('elementos_usados')
    def resta(self):
        self.quantity = self.quantity - self.elementos_usados


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


class estado_kanban_inventario(models.Model):
    _name = 'estado.transferencias'
    _description = "Estado para solicitud de inventario"
    _rec_name = 'name'
    _order = "sequence, name, id"

    @api.model
    def default_get(self, fields):
        """ Hack :  when going from the pipeline, creating a stage with a sales team in
            context should not create a stage for the current Sales Team only
        """
        ctx = dict(self.env.context)
        if ctx.get('default_team_id') and not ctx.get('crm_team_mono'):
            ctx.pop('default_team_id')
        return super(estado_kanban_inventario, self.with_context(ctx)).default_get(fields)

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    is_won = fields.Boolean('Is Won Stage?')
    requirements = fields.Text('Requirements',
                               help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")
    team_id = fields.Many2one('crm.team', string='Sales Team', ondelete='set null',
                              help='Specific team that uses this stage. Other teams will not be able to see or use this stage.')
    fold = fields.Boolean('Folded in Pipeline',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')

    # This field for interface only
    team_count = fields.Integer('team_count', compute='_compute_team_count')

    def _compute_team_count(self):
        for stage in self:
            stage.team_count = self.env['crm.team'].search_count([])
