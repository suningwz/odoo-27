from odoo import _, api, exceptions, fields, models, http
from odoo.http import request
from datetime import datetime

class boton_archivador(models.Model):
    _inherit = "account.move"

    active_boton = fields.Boolean('Active', default=True)
