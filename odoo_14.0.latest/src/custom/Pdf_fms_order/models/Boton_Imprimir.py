from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models



class Imprimir(models.Model):
    _inherit = 'fsm.order'


    def print_report(self):
        print('hola')
