# -*- coding: utf-8 -*-

{
    "name": "Stock Picking Split",
    "version": "17.0.0.1",
    "summary": "",
    "description": """ """,
    "category": "Eticco",
    "website": "https://www.eticco.es/",
    "depends": [
        "base",
        "stock",
        "stock_client_order_ref",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/stock_picking_split_wizard_views.xml",
        "views/stock_picking_views.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
