import requests
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models, http
from odoo.http import request
from datetime import datetime
import json
from xlsxwriter import app
from geopy.geocoders import Nominatim
import time
import math
import urllib.request


class boton_archivador(models.Model):
    _inherit = "account.move"

    active = fields.Boolean('Active', default=True)
    def funcion_libre(self):
        self.active = False