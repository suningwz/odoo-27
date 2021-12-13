# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from odoo.http import Response


class AndroidSync(http.Controller):
    # Ruta personalizada  (' /contacto' )
    # Auth: Permisos de quien puede entrar a esta ruta
    @http.route('/contactus', auth='public', website=True)
    # Nombre de la funcion ojala no involcarla otravez porque se sobre-escribiria
    def contacto_redirect(self):
        # Funcion redirect :  La url del render real
        return request.redirect('/contacto')

    @http.route('/contacto', auth='public', website=True)
    def contacto(self):
        return "Hola mundo "


class WebsiteDirecto(http.Controller):
    @http.route('/productos/<model("product.template"):product>', auth='public', website=True)
    def product(self, product):
        return http.request.render('Android_Sync.product', {
            "product": product
        })


class Hours_(http.Controller):
    @http.route('/api/attendance/hours/<user_id>/<day_week>', auth='user', methods=['GET'])
    def get_attendance_hours(self, user_id, day_week, **kw):
        try:
            calendar_id = http.request.env['hr.employee'].sudo().search(
                [('user_id', '=', int(user_id))]).resource_calendar_id.id
            hours = http.request.env['resource.calendar.attendance'].sudo().search_read(
                [('calendar_id', '=', int(calendar_id)),
                 ('dayofweek', '=', day_week)], ['hour_from', 'hour_to'])

            return self.build_response(hours)
        except Exception as e:
            return self.build_response({'err': str(e)})

    @http.route('/api/attendance', auth='user', methods=['POST'], csrf=False)
    def insert_attendance(self, **kw):
        try:
            attendance = json.loads(
                str(http.request.httprequest.data, 'utf-8'))
            http.request.env['hr.attendance'].create(attendance)
            return self.build_response({'message': 'inserted'})

        except Exception as e:
            return self.build_response({'err': str(e)})

    def build_response(self, entity):
        response = json.dumps(entity, ensure_ascii=False).encode('utf8')
        return Response(response, content_type='application/json;charset=utf-8', status=200)


class Reports(http.Controller):
    @http.route('/get_reports', type="json", auth='user')
    def get_all_reports(self):
        # Get all reports
        reports_rec = request.env['fsm.order'].search([])
        reports = []
        for rec in reports_rec:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'centro_costos': rec.centro_costos.name,
                'person_id': rec.person_id.name,
                'instructions': rec.todo, 
            }
            reports.append(vals)
        data = {'status': 200, 'response': reports, 'message': 'Success', }
        return data
