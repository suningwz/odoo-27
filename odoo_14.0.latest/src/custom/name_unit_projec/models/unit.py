from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class ejemplo_nueva_clase(models.Model):
    _inherit = 'project.task'
    tipo_unidad = fields.Selection([('n/a', 'N/A'), ('atm', 'ATM'), ('edf', 'EDF'), ('ofc', 'OFC')], 'Unidad',
                                   default='n/a')

    @api.onchange('partner_id')
    def selected_named_pject(self):
        self.name = self.partner_id.codigo
        self.tipo_unidad = self.partner_id.tipo_unidad








