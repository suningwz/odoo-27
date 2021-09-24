from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class ejemplo_nueva_clase(models.Model):
    _inherit = 'fsm.order'

    cajero = fields.Char(string='Nombre del cajero', forcesave=1)
    anotaciones = fields.Text(string='restricciones', forcesave=1)
    tipo_unidad = fields.Selection([('n/a', 'N/A'), ('atm', 'ATM'), ('edf', 'EDF'), ('ofc', 'OFC')], 'Unidad',
                                   default='n/a',  forcesave=1)
    tdv = fields.Selection(
        [('n/a', 'N/A'), ('op1', 'ATLAS'), ('op2', 'BRINKS'), ('op3', 'TRANSBANK'), ('op4', 'VATCO'), ('op5', 'SUC')],
        'transporte', default='n/a', forcesave=1)

    centro_costos = fields.Many2one("fsm.location", string="Centro de costos")

    @api.onchange('centro_costos')
    def _centro_costos(self):
        self.location_id = self.centro_costos

    @api.onchange('project_task_id')
    def missing_information(self):
        self.anotaciones = self.project_task_id.partner_id.comment
        self.cajero = self.project_task_id.partner_id.name
        self.tipo_unidad = self.project_task_id.partner_id.tipo_unidad
        self.tdv = self.project_task_id.partner_id.tdv
        self.description = self.project_task_id.modificacion_descripcion

    @api.onchange('person_id')
    def messages_person(self):
        personal =self.env["hr.employee"].search(
            [("name", "=", self.person_id.name)], limit=1
        )
        id = str(self.id).split('_')
        personal.user_id.notify_success(f'Asignacion del proyecto {self.name}')
        id_personal = self.env["res.partner"].search(
            [("name", "=", self.person_id.name)], limit=1
        ).id
        self.env['mail.message'].create({'message_type': "comment",
                                         'subtype_id': 1,
                                         'parent_id': 4172,
                                         'body': f'<span><a href="http://allser.com.co/web#model=res.partner&amp;id={id_personal}" class="o_mail_redirect" data-oe-id="26438" data-oe-model="res.partner" target="_blank">El tecnico lider asignado es: {personal.name}</a></span>',
                                         'record_name': f'{self.name}',
                                         # partner to whom you send notification
                                         'model': self._name,
                                         'res_id': int(id[1]),
                                         })

class descripcion(models.Model):
    _inherit = 'project.task'

    modificacion_descripcion = fields.Text(string="descripcion mod")