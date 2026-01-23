from odoo import _, api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    force_aeat_simplified_invoice = fields.Boolean(
        string="Forzar Factura Simplificada AEAT",
        help="Si está activado, todas las facturas creadas con este diario "
        "serán marcadas como facturas simplificadas para AEAT.",
        default=False,
    )
