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
        worksheet = workbook.add_worksheet("Solicitudes Dineros")
        bold = workbook.add_format({'align': 'center'})

        # worksheet.set_column ancho de la columna ultimo numero
        worksheet.set_column("A:B", 30)
        worksheet.set_column("C:C", 35)
        worksheet.set_column("D:L", 30)

        # Columnas sheet.set_write Nombre y subnombres de las columnas/Ancho de las columnas

        worksheet.write(0, 0, 'NIT PAGADOR', bold)
        worksheet.write(1, 0, '900706219', bold)
        worksheet.write(2, 0, 'Tipo Documento Beneficiario', bold)
        worksheet.write(0, 1, 'TIPO DE PAGO', bold)
        worksheet.write(1, 1, '220', bold)
        worksheet.write(2, 1, 'Nit Beneficiario', bold)
        worksheet.write(0, 2, 'APLICACIÓN', bold)
        worksheet.write(1, 2, 'I', bold)
        worksheet.write(2, 2, 'Nombre Beneficiario', bold)
        worksheet.write(0, 3, 'SECUENCIA DE ENVÍO', bold)
        worksheet.write(1, 3, 'A1', bold)
        worksheet.write(2, 3, 'Tipo Transaccion', bold)
        worksheet.write(0, 4, 'NRO CUENTA A DEBITAR', bold)
        worksheet.write(1, 4, '4620038941', bold)
        worksheet.write(2, 4, 'Código Banco', bold)
        worksheet.write(0, 5, 'TIPO DE CUENTA A DEBITAR', bold)
        worksheet.write(1, 5, 'S', bold)
        worksheet.write(2, 5, 'No Cuenta Beneficiario', bold)
        worksheet.write(0, 6, 'DESCRIPCÓN DEL PAGO', bold)
        worksheet.write(1, 6, 'DINERO1014', bold)
        worksheet.write(2, 6, 'Email', bold)
        worksheet.write(2, 7, 'Documento Autorizado', bold)
        worksheet.write(2, 8, 'Referencia', bold)
        worksheet.write(2, 9, 'OficinaEntrega', bold)
        worksheet.write(2, 10, 'ValorTransaccion', bold)
        worksheet.write(2, 11, 'Fecha de aplicación', bold)
        today = date.today()
        fecha = f'{today.year}{today.month}{today.day}'

        # Valores
        i = 2

        for obj in partners:
            i += 1
            
            # Seccion de Busqueda
            cedula = self.env["hr.employee"].search(
                [("name", "=", obj.personal.name)], limit=1
            )
            #fin de la Seccion
            
            worksheet.write(i, 2, obj.personal.name, bold)
            worksheet.write(i, 6, obj.personal.email, bold)
            worksheet.write(i, 10, obj.bolsa_total, bold)
            worksheet.write(i, 4, '1007', bold)
            worksheet.write(i, 1, cedula.identification_id, bold)
            worksheet.write(i, 3, '37', bold)
            worksheet.write(i, 0, '1', bold)
            worksheet.write(i, 11, fecha, bold)
