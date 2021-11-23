from odoo import models, fields, api
import datetime


class miembros(models.Model):
    _inherit = 'maintenance.team'
    lider = fields.Many2one('res.users','lider')