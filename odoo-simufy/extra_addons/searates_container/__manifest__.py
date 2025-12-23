# -*- coding: utf-8 -*-
{
    "name": "Searates Container Integration",
    "description": """
        Integración de Contenedores Searates
    """,
    "depends": [
        "base",
        "purchase",
        "stock",
        "purchase_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/searates_data.xml",
        "views/purchase_views.xml",
        "views/container_import_views.xml",
    ],
    "author": "Eticco Freelosophy S.L.",
    "installable": True,
    "auto_install": False,
    "application": True,
}
