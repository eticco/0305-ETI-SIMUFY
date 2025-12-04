# -*- coding: utf-8 -*-
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    "name": "Stock Incidence",
    "version": "17.0.0.1",
    "summary": "Módulo Eticco",
    "sequence": 10,
    "description": """ """,
    "category": "Eticco",
    "website": "https://https://www.eticco.es/",
    "depends": [
        "base",
        "stock",
        "delivery",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_incidence_views.xml",
        "wizard/stock_incidence_wizard.xml",
        "views/stock_picking_views.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
