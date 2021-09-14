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


    @api.onchange('project_task_id')
    def missing_information(self):
        self.anotaciones = self.project_task_id.partner_id.comment
        self.cajero = self.project_task_id.partner_id.name
        self.tipo_unidad = self.project_task_id.partner_id.tipo_unidad
        self.tdv = self.project_task_id.partner_id.tdv
        self.description = self.project_task_id.modificacion_descripcion


class descripcion(models.Model):
    _inherit = 'project.task'

    modificacion_descripcion = fields.Text(string="descripcion mod")