# -*- coding: utf-8 -*-
import pytz
from geopy import Nominatim
from odoo import models, fields, api, http
import datetime as DT, datetime
from datetime import timedelta
from odoo.http import request
import random


class examen_tecnico(models.Model):
    _name = 'examen_tecnico.examen_tecnico'
    _description = 'examen_tecnico.examen_tecnico'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    invisible = fields.Boolean(default=False)
    examen = fields.Many2one('creacion_examenes.creacion_examenes')
    hora_ini = fields.Datetime()
    hora_fin = fields.Datetime()
    hora_max = fields.Datetime()
    user_id = fields.Many2one('res.users', string='Presenta')
    cronometro = fields.Float(string='Tiempo')
    presenta = fields.Datetime(string='Fecha de realizacion')
    observaciones = fields.Text()
    lista_preguntas = fields.One2many('preguntas_examen.preguntas_examen', 'opuesto_pe', string='Preguntas')
    aplicacion_examen = fields.Boolean(default=False)

    def cornometro_boton(self):
        self.aplicacion_examen = True
        preguntas = self.examen.lista_preguntas
        lista_pregunta = []
        lista_final = []
        for x in preguntas:
            lista_pregunta.append(x.id)
        num_responder = self.examen.num_preguntas
        lista_final = random.sample(lista_pregunta,num_responder)
        self.lista_preguntas = lista_final

    @api.onchange('hora_ini')
    def inicio_examen(self):
        if not self.hora_ini:
            naive = DT.datetime.now()
            utc = pytz.utc
            gmt5 = pytz.timezone('Etc/GMT+5')
            hora = str(utc.localize(naive).astimezone(gmt5))
            hora = hora.split('.')
            hora = hora[0]
            hora2 = str(utc.localize(naive).astimezone(gmt5) + timedelta(hours=1))
            hora2 = hora2.split('.')
            hora2 = hora2[0]
            self.hora_ini = hora
            self.hora_max = hora2
            print(self.hora_ini)
            print(self.hora_max)

    def confirmar_examen(self):
        if self.examen:
            self.name = self.examen.name
            naive = self.examen.hora
            utc = pytz.utc
            gmt5 = pytz.timezone('Etc/GMT+5')
            hora1 = utc.localize(naive).astimezone(gmt5).strftime('%H:%M')
            naive = self.examen.hora2
            utc = pytz.utc
            gmt5 = pytz.timezone('Etc/GMT+5')
            hora2 = utc.localize(naive).astimezone(gmt5).strftime('%H:%M')
            horai = self.hora_ini.strftime('%H:%M')
            if hora1 > horai:
                view = self.env.ref('sh_message.sh_message_wizard')
                view_id = view and view.id or False
                context = dict(self._context or {})
                context[
                    'message'] = "Aun no se puede presentar el examen"
                return {
                    'name': 'ADVERTENCIA',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_model': 'form',
                    'res_model': 'sh.message.wizard',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    'target': 'new',
                    'context': context,
                }
            elif hora1 < horai:
                if hora2 > horai:
                    print('se puede ejecutar')
                    self.invisible = True
                    tiempo = float(self.examen.tiempo * self.examen.num_preguntas)
                    self.cronometro = tiempo
                    self.presenta = datetime.datetime.now()
                    self.user_id = self.env.user
                    self.observaciones = self.examen.recomendaciones
                elif hora2 < horai:
                    view = self.env.ref('sh_message.sh_message_wizard')
                    view_id = view and view.id or False
                    context = dict(self._context or {})
                    context[
                        'message'] = "No se puede presentar el examen"
                    return {
                        'name': 'ADVERTENCIA',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_model': 'form',
                        'res_model': 'sh.message.wizard',
                        'views': [(view.id, 'form')],
                        'view_id': view.id,
                        'target': 'new',
                        'context': context,
                    }

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


class creacion_examenes(models.Model):
    _name = 'creacion_examenes.creacion_examenes'
    _description = 'creacion_examenes.creacion_examenes'

    name = fields.Char(required=True)
    tiempo = fields.Integer(required=True)
    formato_tiempo = fields.Selection([('H', 'Horas'), ('M', 'Minutos')])
    num_preguntas = fields.Integer(required=True)
    recomendaciones = fields.Text()
    nota_aprovatoria = fields.Integer(required=True, size=2,
                                      help='la nota se debe tomar de 1 a 100, si se pasa de ese valor quedara la nota en 100')
    lista_preguntas = fields.One2many('preguntas_examen.preguntas_examen', 'opuesto_examenes', string='Listado')
    hora = fields.Datetime(required=True)
    hora2 = fields.Datetime(required=True)

    @api.onchange('nota_aprovatoria')
    def redonder_nota(self):
        nota = self.nota_aprovatoria
        if nota >= 100:
            self.nota_aprovatoria = 100


class preguntas_examen(models.Model):
    _name = 'preguntas_examen.preguntas_examen'
    _description = 'preguntas_examen.preguntas_examen'

    name = fields.Text()
    respuesta = fields.Text()
    respuesta1 = fields.Text()
    respuesta2 = fields.Text()
    respuesta3 = fields.Text()
    respuesta_correcta = fields.Selection([('1', 'A'),
                                           ('2', 'B'),
                                           ('3', 'C'),
                                           ('4', 'D')])
    respuesta_representante = fields.Selection([('1', 'A'),
                                                ('2', 'B'),
                                                ('3', 'C'),
                                                ('4', 'D')])
    opuesto_examenes = fields.Many2one('creacion_examenes.creacion_examenes')
    opuesto_pe = fields.Many2one('examen_tecnico.examen_tecnico')


# esto es un controlador que se usar para recibir los paremtros
# mediante un archivo JSON del front enviado por JS para poder calcular la geolocalizacion
class odoocontroler(http.Controller):
    @http.route(['/ajax_cronometro'], type='json', auth='public', methods=['POST'])
    def geolocalizacion(self, **kw):
        p = {
            "Estatus": "0k"
        }
        return p
