{
    'name': 'Reporte pdf para fms',
    'summary': 'Diseño para generar los pdf para fms',
    'version': '14.0.1',
    'author': 'Allser',
    'sequence': 0,
    'depends': ['base', 'fieldservice', 'stock','hr_expense', 'hr',
                ],
    'data': [
        'views/Pdf_acta_fms_cliente.xml',
        'views/Pdf_acta_fms_cliente.xml',
        'views/pdf_menu.xml'
    ],
    'installable': True,
    'application': True,
}



