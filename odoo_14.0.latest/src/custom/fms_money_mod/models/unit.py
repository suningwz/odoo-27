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

class informes_gastos(models.Model):
    _inherit = 'hr.expense.sheet'

    def approve_expenses(self):
        self.employee_id.bolsa_total = (self.employee_id.bolsa_total - self.total_amount)
        self.approve_expense_sheets()

class vista_bolsa(models.Model):
    _inherit = 'fsm.order'

    gastos_tecnico = fields.One2many('hr.expense', 'gastos_opuesto', readonly=1)
    bolsa_total_tecnico = fields.Integer('total')

    @api.onchange('person_id')
    def default_bag(self):
        persona = self.env["hr.employee"].search(
            [("name", "=", self.person_id.name)], limit=1
        )
        self.bolsa_total_tecnico = persona.bolsa_total

        elements = self.env["hr.expense"].search(
            [("employee_id", "=", self.person_id.name)]
        )
        if not elements:
            print('vacio')
        else:
            x = str(elements).split('(')
            y = len(x)
            print(y)
            x = x[1].split(')')
            x = x[0].split(',')
            y = len(x)
            print(y)
            if int(y) < 1:
                print(x)
            else:
                for j in range(y):
                    print(x[j])
                    if not x[j]:
                        print('vacio')
                    else:
                        resultado = x[j]
                        resultado = int(resultado)
                        self.gastos_tecnico =  [(4, resultado)]

class gastos(models.Model):
    _inherit = 'hr.expense'

    gastos_opuesto = fields.Many2one('fsm.order', string="", invisible="True")
