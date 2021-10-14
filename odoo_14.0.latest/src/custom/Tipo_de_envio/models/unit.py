from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models
from odoo.addons.stock.models import stock_picking


class quienelabora(models.Model):
    _inherit = 'stock.picking'

    # Funcion para invocar una funcion llamando una clase de un archivo externo
    # Recordar como importar el modulo
    def button_validate1(self):
        if not self.quien_elabora:
            var = stock_picking
            var.Picking.button_validate(self)
            self.quien_elabora = str(self.env.user.name)

    quien_elabora = fields.Char(string='Elabora')

    local_en_sitio = fields.Char(string='Local en Sitio')

    local_motorizado = fields.Char(string='Local Motorizado',
                                   default="https://web.mensajerosurbanos.com/iniciar-sesion")

    local_vehiculo = fields.Char(string='Local Vehiculo',
                                 default="https://docs.google.com/spreadsheets/d/1PNczfqyKZwxJ6Af5xvtuNiYpAPAQidbtygp3OGqBMp0/edit#gid=530808139")

    ejecucion = fields.Selection(
        [("r1", "Envio Nacional"), ("r2", "Local en Sitio"), ("r3", "Local Motorizado"), ("r4", "Local Vehiculo")],
        string="¿Que servicio desea?")

    Transporte = fields.Selection(
        [('f1', 'Servientrega'),
         ('f2', 'GoPack365')],
        string='Envio Nacional')

    urlServientrega = fields.Char(string='Servientrega',
                                  default="https://canales.servientrega.com/sisclinet/login.aspx")
    urlGoPack365 = fields.Char(string='GoPack365', default="http://www.gopack365.com/index.php")
