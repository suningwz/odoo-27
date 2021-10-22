import requests
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models, http


class campo_relacion_cobreo(models.Model):
    _inherit = 'fsm.order'

    ventas_fsm = fields.One2many('sale.order', 'fsm_id', string= 'Tabla para crear la orden de corbo')
    def crear_cotizacion(self):
        if not self.centro_costos:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] ="Verificar el centro de costos"
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
            action = self.env.ref("sale.action_orders")
            result = action.read()[0]
            # override the context to get rid of the default filtering
            result["context"] = {
                "default_partner_id": self.centro_costos.owner_id.id,
                "default_fms_id": self.id,
            }
            res = self.env.ref("sale.view_order_form", False)
            result["views"] = [(res and res.id or False, "form")]
            return result

class _sale_order_line(models.Model):
    _inherit = 'sale.order'
    fsm_id = fields.Many2one('fsm.order')
