{
    'name': 'Tipo de Envio',
    'summary': 'Diseño para generar que tipo de envio se desea',
    'version': '14.0.1',
    'author': 'Allservice Rhino',
    'sequence': 0,
    'depends': ['base', 'fieldservice', 'stock', 'hr_expense', 'hr',
                ],
    'data': [
        'views/Quien_Elabora.xml',
        'views/Envio.xml',
    ],
    'installable': True,
    'application': True,
}
