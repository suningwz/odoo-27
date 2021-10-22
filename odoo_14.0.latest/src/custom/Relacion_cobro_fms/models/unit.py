import requests
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models, http


class campo_relacion_cobreo(models.Model):
    _inherit = 'fsm.order'

    ventas_fsm = fields.One2many('sale.order', 'fsm_id', string= 'Tabla para crear la orden de corbo')
    def crear_cotizacion(self):
        """
        This function returns an action that displays a full FSM Order
        form when creating an FSM Order from a project.
        """
        action = self.env.ref("sale.action_orders")
        result = action.read()[0]
        # override the context to get rid of the default filtering
        result["context"] = {
            "partner_id": self.centro_costos.owner_id.id,
        }
        res = self.env.ref("sale.view_order_form", False)
        result["views"] = [(res and res.id or False, "form")]
        return result

class _sale_order_line(models.Model):
    _inherit = 'sale.order'
    fsm_id = fields.Many2one('fsm.order')
