{
    'name': 'Boton de archivar',
    'summary': 'Diseño para archivar elementos en servicio de campo y inventario',
    'version': '14.0.1',
    'author': 'Allser',
    'sequence': 0,
    'depends': ['base', 'fieldservice', 'stock', 'hr_expense',
                ],
    'data': [
        'views/unit.xml',
        'views/unit2.xml',
        'views/Archivador_Gastos.xml',
    ],
    'installable': True,
    'application': True,
}
