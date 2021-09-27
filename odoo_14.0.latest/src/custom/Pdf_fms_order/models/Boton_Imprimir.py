from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class Imprimir(models.Model):
    _inherit = 'fsm.order'

    def print_report(self):
        if not self.firma:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] ="Falta ingresar la firma"
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
            return self.env.ref('Pdf_fms_order.reportepdf').report_action(self)
