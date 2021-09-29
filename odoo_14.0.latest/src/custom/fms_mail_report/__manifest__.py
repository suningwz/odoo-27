

{
    'name': 'Fms Mails ',
    "summary": "Este modulo se utiliza para que se envie el correo electronico a la persona que firma el acta",
    'version': '14.0.1',
    'author': 'Allser',
    'sequence': 0,
    'depends': ['base', 'fieldservice', 'project',
                ],
    'data': [
        'views/codigo.xml',
        'views/mail_template.xml',
    ],
    'application': True,
}



