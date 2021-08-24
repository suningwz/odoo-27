from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class almacen_tecnico(models.Model):
    _inherit = 'fsm.order'

    inventario = fields.One2many('stock.quant','opuesto', readonly=1)

    @api.onchange('person_id')
    def default_inventario(self):
        warehouse_ids = self.env["stock.warehouse"].search(
            [("name", "=", self.person_id.name)], limit=1
        )
        elements = self.env["stock.quant"].search(
            [("location_id", "=", f"{warehouse_ids.code}/Existencias")]
        )
        if not elements:
            print('vacio')
        else:
            x = str(elements).split('(')
            y = len(x)
            print(y)
            x = x[1].split(')')
            x = x[0].split(',')
            y = len(x)
            print(y)
            if int(y) < 1:
                print(x)
            else:
                for j in range(y):
                    print(x[j])
                    if not x[j]:
                        print('vacio')
                    else:
                        resultado = x[j]
                        resultado = int(resultado)
                        self.inventario = [(4, resultado)]

class opuesto_tecnico(models.Model):
    _inherit = 'stock.quant'

    opuesto = fields.Many2one('fsm.order', string="", readonly="True")









