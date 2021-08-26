from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError, AccessError


class video_mano(models.Model):
    _name = 'solicitudes.bolsa'

    bolsa_dineros = fields.Integer('dinero a solicitar')
    bolsa_total = fields.Integer('total')
    personal = fields.Many2one('res.partner', required = 1)
    estado = fields.Selection([
        ('p1', "Solicitado"),
        ('p2', "Aprobado"),
        ('p3', "Cancelado"),
    ], default='p1')
    motivo = fields.Text()
    def _default_employee(self):
        return self.env.user.employee_id

    solicitado = fields.Many2one('hr.employee', default=_default_employee)
    solicitud_opuesto = fields.Many2one('fsm.order', string="", invisible="True")

    @api.onchange('personal')
    def persona(self):
        persona = self.env["hr.employee"].search(
            [("name", "=", self.personal.name)], limit=1
        )
        self.bolsa_total = persona.bolsa_total

    def aprovacion_exporte(self):
        persona = self.env["hr.employee"].search(
            [("name", "=", self.personal.name)], limit=1
        )
        valor = self.bolsa_dineros
        valor2 = self.bolsa_total
        valor = valor2 + valor
        if valor == 150000:
            self.bolsa_dineros = 0
            self.bolsa_total = valor
            persona.bolsa_total = self.bolsa_total
        elif valor < 150000:
            self.bolsa_dineros = 0
            raise ValidationError(f'el valor de: {valor} es menor al maximo')
        elif valor > 150000:
            if valor <= 300000:
                self.bolsa_dineros = 0
                self.bolsa_total = valor
                persona.bolsa_total = self.bolsa_total
            elif valor > 300000:
                self.bolsa_dineros = 0
                raise ValidationError(f'el valor de: {valor} excede el tope')

        self.estado = 'p2'

    def cancelado(self):
        self.estado = 'p3'
