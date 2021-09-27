from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class Imprimir(models.Model):
    _inherit = 'fsm.order'

    def print_report(self):
        if not self.firma or not self.q_firma or not self.cc_q_firma:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] ="Verificar por favor en el campo de Ejecucion/Firma que requerimiento falta para completar"
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


