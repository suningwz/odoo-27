import self as self
from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class quienelabora(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if not self.quien_elabora:
            self.quien_elabora = str(self.env.user.name)

    quien_elabora = fields.Char(string='Elabora')

    local_en_sitio = fields.Char(string='Local en Sitio')

    local_motorizado = fields.Char(string='Elabora', default="https://web.mensajerosurbanos.com/iniciar-sesion")

    local_vehiculo = fields.Char(string='Elabora')

    ejecucion = fields.Selection(
        [("r1", "Envio Nacional"), ("r2", "Local en Sitio"), ("r3", "Local Motorizado"), ("r4", "Local Vehiculo")],
        string="¿Que servicio desea?")

    Transporte = fields.Selection(
        [('f1', 'Servientrega'),
         ('f2', 'GoPack365')],
        string='Envio Nacional')

    urlServientrega = fields.Char(String='Servientrega',
                                  default="https://canales.servientrega.com/sisclinet/login.aspx")
    urlGoPack365 = fields.Char(String='GoPack365', default="http://www.gopack365.com/index.php")
