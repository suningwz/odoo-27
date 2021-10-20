import requests
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models, http


class campo_relacion_cobreo(models.Model):
    _inherit = 'fsm.order'

    ventas_fsm = fields.One2many('sale.order', 'fsm_id', string= 'Tabla para crear la orden de corbo')


class _sale_order_line(models.Model):
    _inherit = 'sale.order'
    fsm_id = fields.Many2one('fsm.order')
