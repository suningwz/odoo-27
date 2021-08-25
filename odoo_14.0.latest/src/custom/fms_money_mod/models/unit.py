from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError, AccessError


class bolsa_tecnicos(models.Model):
    _inherit = 'hr.employee'

    bolsa_dineros = fields.Integer('dinero a ingresar')
    bolsa_total = fields.Integer('total', readonly=1,forcesave=1)

    def ingresar_dinero(self):
       valor = self.bolsa_dineros
       valor2 = self.bolsa_total
       valor = valor2 + valor
       if valor == 150000:
           self.bolsa_dineros = 0
           self.bolsa_total = valor
       elif valor < 150000:
           self.bolsa_dineros = 0
           raise ValidationError(f'el valor de: {valor} es menor al maximo')
       elif valor > 150000:
           if valor <= 300000:
               self.bolsa_dineros = 0
               self.bolsa_total = valor
           elif valor > 300000:
               self.bolsa_dineros = 0
               raise ValidationError(f'el valor de: {valor} excede el tope')








