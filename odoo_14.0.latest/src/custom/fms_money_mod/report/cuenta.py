from odoo import models, fields, api

class User(models.Model):
    _inherit = 'hr.employee'
    
    Cuenta = fields.Char( String= 'Cuenta Bancaria')
    