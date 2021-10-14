{
    'name': 'Vizualizar el inventario',
    'summary': 'Diseño para vizualizar los elementos de stock de la persona',
    'version': '14.0.1',
    'author': 'Allser',
    'sequence': 0,
    'depends': ['base', 'fieldservice', 'stock',
                ],
    'data': [
        'views/unit.py',
        'views/unit2.xml',
        'views/unit3.xml',
        'views/js_template.xml',
        'views/vista_kanban.xml',
        'views/almacen_tercero.xml',
        'views/view_mod_tree.xml',
    ],
    'installable': True,
    'application': True,
}


