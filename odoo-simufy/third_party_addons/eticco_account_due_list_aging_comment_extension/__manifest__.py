# -*- coding: utf-8 -*-

{
    "name": "Eticco Account Due List Aging Comment Extension",
    "images": [],
    "summary": """Gestión de comentarios de efectos""",
    "description": """
        Los módulos account_due_list se descargaran de https://github.com/OCA/account-payment.git
    """,
    "author": "Eticco Freelosophy S.L.",
    "license": "AGPL-3",
    "website": "http://www.eticco.es",
    "category": "Eticco",
    "version": "17.0.0.1",
    "depends": [
        "account_due_list",
        "account_due_list_aging_comment",
        "account_due_list_payment_mode",
        "account_payment_partner",
    ],
    "data": [
        "views/account_move_line_view.xml",
    ],
    "application": True,
    "installable": True,
}
