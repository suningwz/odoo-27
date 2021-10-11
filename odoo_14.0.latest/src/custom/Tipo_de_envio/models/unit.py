from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class quienelabora(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if not self.quien_elabora:
            self.env.user = self.quien_elabora

    quien_elabora = fields.Many2one('res.partner', string='Elabora')


class envio(models.Model):
    _inherit = 'stock.picking'

    Transporte = fields.Selection(
        [('f1', 'Coodinadora'),
         ('f2', 'Servientrega'),
         ('f3', 'Envia'),
         ('f4', 'TCC'),
         ('f5', 'Deprisa'),
         ('f6', 'InterRapidisimo'),
         ('f7', 'DHL'),
         ('f8', '472'),
         ('f9', 'Red Servi'),
         ('f10', 'FedEx'),
         ('f11', 'Saferbo')],
        string=' Tipo de Despachadora')
