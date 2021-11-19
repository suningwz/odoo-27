
from odoo import models, fields, api


class User(models.Model):
    _inherit = 'hr.employee'

    Cuenta = fields.Char(String='Cuenta Bancaria del Empleado')


    @api.onchange('Cuenta')
    def igual_cuentas(self):
        
     # Busqueda para encontrar el nombre de la cuenta que este en conectado en ese momento
        self.user_id.address_home_id.bank_ids = [ (0, 0, {'acc_number': self.Cuenta})]
        cedula = self.env["res.users"].search(
            [("name", "=", self.name)], limit=1
        )
        # Busqueda para encontrar la tabla res.partner.bank y a su vez encontrar los numeros
        # que esten asociada a ella en la tabla de acc_number 
        cedula.employee_bank_account_id = self.env["res.partner.bank"].search(
            [("acc_number", "=", self.Cuenta)], limit=1
        ).id
