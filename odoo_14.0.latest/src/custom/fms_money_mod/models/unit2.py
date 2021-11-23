from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError, AccessError


class video_mano(models.Model):
    _name = 'solicitudes.bolsa'

    bolsa_dineros = fields.Integer('dinero a solicitar')
    bolsa_total = fields.Integer('total')
    personal = fields.Many2one('res.partner', required=1)
    estado = fields.Selection([
        ('p1', "Solicitado"),
        ('p2', "Aprobado"),
        ('p3', "Cancelado"),
        ('p4', "Guardado")
    ], default='p1')
    motivo = fields.Text()

    def _default_employee(self):
        return self.env.user.employee_id

    def _dato(self):
        dato = self.env["res.partner"].search(
            [("name", "=", self.env.user.name)], limit=1
        )
        dato = dato.function
        print(dato)
        return dato

    solicitado = fields.Many2one('hr.employee', default=_default_employee)
    solicitud_opuesto = fields.Many2one('fsm.order', string="", invisible="True")
    puesto = fields.Char(string='Nombre del cajero', compute=_dato)

    @api.onchange('personal')
    def persona(self):
        persona = self.env["hr.employee"].search(
            [("name", "=", self.personal.name)], limit=1
        )
        self.bolsa_total = persona.bolsa_total

    def aprovacion_exporte(self):
        if self.estado == 'p2':
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context[
                'message'] = "La solicitud ha sido aprobada, si desea aprobar otra solicitud, haga click en el botón 'Crear'"
            return {
                'name': 'ADVERTENCIA',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_model': 'form',
                'res_model': 'sh.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
            }
        else:
            persona = self.env["hr.employee"].search(
                [("name", "=", self.personal.name)], limit=1
            )
            valor = self.bolsa_dineros
            valor2 = self.bolsa_total
            valor = valor2 + valor
            if valor == 150000:
                self.bolsa_total = valor
                persona.bolsa_total = self.bolsa_total
            elif valor < 150000:
                raise ValidationError(f'El valor de: {valor} es menor al maximo')
            elif valor > 150000:
                if valor <= 300000:
                    self.bolsa_total = valor
                    persona.bolsa_total = self.bolsa_total
                elif valor > 300000:
                    raise ValidationError(f'El valor de: {valor} excede el tope')

            self.estado = 'p2'

    def cancelado(self):
        self.estado = 'p3'

    def Notificacion_gastos(self):
        name_location = f"{self.solicitado.expense_manager_id.name}"
        personal = self.env["hr.employee"].search(
            [("name", "=", name_location)], limit=1
        )
        personal.user_id.notify_success(f'Nueva solicitud de dineros')

    @api.constrains('bolsa_dineros')
    def cambio_guardado(self):
        self.estado = 'p4'
