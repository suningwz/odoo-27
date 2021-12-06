# -*- coding: utf-8 -*-
from odoo import models, fields, api


class examen_tecnico(models.Model):
    _name = 'examen_tecnico.examen_tecnico'
    _description = 'examen_tecnico.examen_tecnico'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    examen = fields.Many2one('creacion_examenes.creacion_examenes')

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
    @api.onchange('nota_aprovatoria')
    def redonder_nota(self):
        nota = self.nota_aprovatoria
        if nota >= 100:
            self.nota_aprovatoria = 100


class preguntas_examen(models.Model):
    _name = 'preguntas_examen.preguntas_examen'
    _description = 'preguntas_examen.preguntas_examen'

    name = fields.Char()
    respuesta = fields.Char()
    respuesta1 = fields.Char()
    respuesta2 = fields.Char()
    respuesta3 = fields.Char()
    respuesta4 = fields.Char()
    respuesta5 = fields.Char()
    respuesta_correcta = fields.Selection([('1', '1'),
                                           ('2', '2'),
                                           ('3', '3'),
                                           ('4', '4'),
                                           ('5', '5'),
                                           ('6', '6')])
    respuesta_representante = fields.Selection([('1', '1'),
                                                ('2', '2'),
                                                ('3', '3'),
                                                ('4', '4'),
                                                ('5', '5'),
                                                ('6', '6')])
    opuesto_examenes = fields.Many2one('creacion_examenes.creacion_examenes')