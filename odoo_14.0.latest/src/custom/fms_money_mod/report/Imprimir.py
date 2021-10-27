from odoo import models
from datetime import datetime, date


class Clientes(models.Model):
    _inherit = "solicitudes.bolsa"

    def btn_generar_reporte(self):
        report_obj = self.env.ref("fms_money_mod.Excel_xlsx")
        return report_obj.report_action({})


class Excel(models.AbstractModel):
    _name = "report.fms_money_mod.clientes_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Reporte"

    # Primer numero Columna-vertical
    # Segundo Numero Fila-horizontal

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Solicitudes Dineros")
        bold = workbook.add_format({'align': 'center'})

        # Columnas sheet.set_write Nombre y subnombres de las columnas/Ancho de las columnas
        # sheet.set_column_pixels ultimo numero
        sheet.set_column_pixels(0, 0, 215)
        sheet.write(0, 0, 'NIT PAGADOR', bold)
        sheet.write(1, 0, '900706219', bold)
        sheet.write(2, 0, 'Tipo Documento Beneficiario', bold)
        sheet.set_column_pixels(0, 1, 215)
        sheet.write(0, 1, 'TIPO DE PAGO', bold)
        sheet.write(1, 1, '220', bold)
        sheet.write(2, 1, 'Nit Beneficiario', bold)
        sheet.set_column_pixels(0, 2, 215)
        sheet.write(0, 2, 'APLICACIÓN', bold)
        sheet.write(1, 2, 'I', bold)
        sheet.write(2, 2, 'Nombre Beneficiario', bold)
        sheet.set_column_pixels(0, 3, 225)
        sheet.write(0, 3, 'SECUENCIA DE ENVÍO', bold)
        sheet.write(1, 3, 'A1', bold)
        sheet.write(2, 3, 'Tipo Transaccion', bold)
        sheet.set_column_pixels(0, 4, 215)
        sheet.write(0, 4, 'NRO CUENTA A DEBITAR', bold)
        sheet.write(1, 4, '4620038941', bold)
        sheet.write(2, 4, 'Código Banco', bold)
        sheet.set_column_pixels(0, 5, 215)
        sheet.write(0, 5, 'TIPO DE CUENTA A DEBITAR', bold)
        sheet.write(1, 5, 'S', bold)
        sheet.write(2, 5, 'No Cuenta Beneficiario', bold)
        sheet.set_column_pixels(0, 6, 215)
        sheet.write(0, 6, 'DESCRIPCÓN DEL PAGO', bold)
        sheet.write(1, 6, 'DINERO1014', bold)
        sheet.write(2, 6, 'Email', bold)
        sheet.set_column_pixels(0, 7, 215)
        sheet.write(2, 7, 'Documento Autorizado', bold)
        sheet.set_column_pixels(0, 8, 215)
        sheet.write(2, 8, 'Referencia', bold)
        sheet.set_column_pixels(0, 9, 215)
        sheet.write(2, 9, 'OficinaEntrega', bold)
        sheet.set_column_pixels(0, 10, 215)
        sheet.write(2, 10, 'ValorTransaccion', bold)
        sheet.set_column_pixels(0, 11, 215)
        sheet.write(2, 11, 'Fecha de aplicación', bold)
        today = date.today()
        fecha = f'{today.year}{today.month}{today.day}'

        # Valores
        i = 2

        for obj in partners:
            i += 1
            sheet.write(i, 2, obj.personal.name, bold)
            sheet.write(i, 6, obj.personal.email, bold)
            sheet.write(i, 10, obj.bolsa_total, bold)
            sheet.write(i, 4, '1007', bold)
            sheet.write(i, 3, '37', bold)
            sheet.write(i, 0, '1', bold)
            sheet.write(i, 11, fecha, bold)

