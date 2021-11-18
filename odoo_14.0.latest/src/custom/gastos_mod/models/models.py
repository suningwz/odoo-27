# -*- coding: utf-8 -*-

from odoo import models, fields, api


class gastos_mod(models.Model):
    _inherit = 'hr.expense'
    valor_factura = fields.Float('Valor de la factura')
    diferecia_valores = fields.Float('Diferencia entre las facturas')

    @api.onchange('valor_factura')
    def diferecia_de_valores(self):
        valor1 = self.unit_amount - self.valor_factura
        self.diferecia_valores = valor1
        self.payment_mode = 'company_account'
