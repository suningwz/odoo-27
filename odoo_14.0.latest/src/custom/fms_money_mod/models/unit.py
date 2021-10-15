from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError, AccessError


class bolsa_tecnicos(models.Model):
    _inherit = 'hr.employee'

    bolsa_dineros = fields.Integer('dinero a ingresar')
    bolsa_total = fields.Integer(string='Total', readonly=1, forcesave=1)

    def ingresar_dinero(self):
       valor = self.bolsa_dineros
       valor2 = self.bolsa_total
       valor = valor2 + valor
       if valor == 150000:
           self.bolsa_dineros = 0
           self.bolsa_total = valor
       elif valor < 150000:
           self.bolsa_dineros = 0
           raise ValidationError(f'El valor minimo para ingresar es de  150000'
                                 f'Actualmente se esta ingresando {valor}')
       elif valor > 150000:
           if valor <= 300000:
               self.bolsa_dineros = 0
               self.bolsa_total = valor
           elif valor > 300000:
               self.bolsa_dineros = 0
               raise ValidationError(f'El valor maximo que se puede es de 300000 '
                                     f'Actualmente se esta ingresando {valor}')

class informes_gastos(models.Model):
    _inherit = 'hr.expense.sheet'

    def approve_expenses(self):
        self.employee_id.bolsa_total = (self.employee_id.bolsa_total - self.total_amount)
        self.approve_expense_sheets()

class vista_bolsa(models.Model):
    _inherit = 'fsm.order'

    gastos_tecnico = fields.One2many('hr.expense', 'gastos_opuesto')
    bolsa_total_tecnico = fields.Integer('Total')
    solicitudes_dineros = fields.One2many('solicitudes.bolsa', 'solicitud_opuesto')

    @api.onchange('person_id')
    def default_bag(self):
        persona = self.env["hr.employee"].search(
            [("name", "=", self.person_id.name)], limit=1
        )
        self.bolsa_total_tecnico = persona.bolsa_total

class gastos(models.Model):
    _inherit = 'hr.expense'

    gastos_opuesto = fields.Many2one('fsm.order', string="", invisible="True")
    seleccion_proyecto = fields.Many2one('fsm.order', string='Relacione la orden de servicio')
    current_user = fields.Char('nombre', default=lambda self: self.env.user.name)

class bolsa_error(models.Model):
    _inherit = 'hr.employee.public'

    bolsa_dineros = fields.Integer('dinero a ingresar')
    bolsa_total = fields.Integer('total', readonly=1, forcesave=1)
