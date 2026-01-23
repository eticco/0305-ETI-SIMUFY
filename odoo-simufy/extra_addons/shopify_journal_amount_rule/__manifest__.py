# -*- coding: utf-8 -*-
{
    "name": "Shopify Journal Amount Rule",
    "description": """
        Módulo para definir reglas basadas en montos para diarios contables.
    """,
    "depends": ["common_connector_library", "account_intrastat"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_workflow_process_view.xml",
    ],
    "author": "Eticco Freelosophy S.L.",
    "installable": True,
    "auto_install": False,
    "application": False,
}
