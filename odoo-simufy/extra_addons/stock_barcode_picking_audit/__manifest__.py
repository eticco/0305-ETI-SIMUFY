# -*- coding: utf-8 -*-
# Este fichero carga configuración de Odoo
{
    "name": "Stock Barcode Picking Audit",
    "description": """
        Módulo para auditar las operaciones realizadas en los albaranes de stock desde el módulo
        de código de barras. Permite registrar quién ha hecho cada albarán.
    """,
    "depends": [
        "base",
        "product",
        "stock",
        "sale_stock",
        "stock_barcode",
    ],
    "data": [
        "views/stock_picking_views.xml",
    ],
    "author": "Eticco Freelosophy S.L.",
    "installable": True,
    "auto_install": False,
    "application": False,
}
