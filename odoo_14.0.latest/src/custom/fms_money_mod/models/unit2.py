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
    def _default_employee(self):
        return self.env.user.employee_id

    solicitado = fields.Many2one('hr.employee', default=_default_employee)
    solicitud_opuesto = fields.Many2one('fsm.order', string="", invisible="True")

    def prueba(self):
        print('holi')

