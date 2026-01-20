# noinspection PyStatementEffect
{
    "name": "Stock Client Order Ref",
    "summary": """Adds a customer reference field to the stock picking record""",
    "author": "Eticco",
    "category": "Warehouse",
    "version": "17.0.0.0.1",
    "license": "OPL-1",
    "currency": "EUR",
    "depends": ["stock", "sale", "sale_stock"],
    "data": ["views/stock_picking_views.xml", "report/stock_picking_templates.xml"],
}
