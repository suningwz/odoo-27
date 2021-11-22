from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class ejemplo_nueva_clase(models.Model):
    _inherit = 'res.partner'

    codigo = fields.Char('Código')
    tipo_unidad = fields.Selection([('n/a', 'N/A'), ('atm', 'ATM'), ('edf', 'EDF'), ('ofc', 'OFC')], 'Unidad',
                                   default='n/a')
    tdv = fields.Selection(
        [('n/a', 'N/A'), ('op1', 'ATLAS'), ('op2', 'BRINKS'), ('op3', 'TRANSBANK'), ('op4', 'VATCO'), ('op5', 'SUC')],
        'transporte', default='n/a')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            if operator in positive_operators:
                locations = self.search([
                    '|',
                    ('codigo', operator, name),
                    ('name', operator, name)
                ])
        else:
            locations = self.search(args, limit=limit)
        return locations.name_get()
