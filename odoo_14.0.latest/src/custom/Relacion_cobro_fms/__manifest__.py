{
    'name': 'Relacion de cobro',
    'summary': 'Se crea la seccion de cobros para que pase a ventas',
    'version': '14.0.1',
    'author': 'Allservice Rhino',
    'sequence': 0,
    'depends': ['base', 'sale_management', 'fieldservice'
                ],
    'data': [
        'views/page.xml',
        'views/unit.xml',
    ],
    'installable': True,
    'application': True,
}