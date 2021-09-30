{
    'name': 'Reporte pdf para Inventario/Orden de salida',
    'summary': 'Diseño para generar los pdf para fms',
    'version': '14.0.1',
    'author': 'Allservice Rhino',
    'sequence': 0,
    'depends': ['base', 'fieldservice', 'stock', 'hr_expense', 'hr',
                ],
    'data': [
        'views/Pdf_Orden_de_Salida.xml',
        'views/Pdf_menu.xml',

    ],
    'installable': True,
    'application': True,
}
