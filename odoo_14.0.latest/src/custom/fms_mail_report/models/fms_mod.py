import base64

from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models





class ejemplo_nueva_clase(models.Model):
    _inherit = 'fsm.order'
    correo_representante = fields.Char()
    datos_personales = fields.Boolean(default=False)

    def sed_mails(self):
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
            report_template_id = self.env.ref(
                'Pdf_fms_order.reportepdf')._render_qweb_pdf(self.id)
            data_record = base64.b64encode(report_template_id[0])
            ir_values = {
                'name': "Customer Report",
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            }
            data_id = self.env['ir.attachment'].create(ir_values)
            template_id_mail = self.env.ref("fms_mail_report.email_card_email").id
            template = self.env['mail.template'].browse(template_id_mail)
            template.attachment_ids = [(6, 0, [data_id.id])]
            email_values = {'email_to': self.correo_representante,
                            'email_from': 'alertas@allser.com.co'}
            if not template_id_mail:
                print(template_id_mail)
            else:
                template.send_mail(self.id, email_values=email_values, force_send=True)
            template.attachment_ids = [(3, data_id.id)]
            return True

