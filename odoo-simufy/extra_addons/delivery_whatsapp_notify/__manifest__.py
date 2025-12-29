# -*- coding: utf-8 -*-
{
    "name": "Delivery WhatsApp Notify",
    "description": """
        Módulo para notificar a los clientes vía WhatsApp sobre el estado de sus entregas.
    """,
    "depends": ["stock", "delivery_state", "stock_barcode", "whatsapp"],
    "data": [
        "data/ir_con_data.xml",
        "data/whatsapp_notify_state_data.xml",
        "data/whatsapp_template_data.xml",
        "security/ir.model.access.csv",
        "views/delivery_carrier_view.xml",
    ],
    "author": "Eticco Freelosophy S.L.",
    "installable": True,
    "auto_install": False,
    "application": False,
}
