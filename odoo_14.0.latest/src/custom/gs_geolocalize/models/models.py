# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 7))
