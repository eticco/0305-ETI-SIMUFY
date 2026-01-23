from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _is_aeat_simplified_invoice(self):
        return (
            self.journal_id.force_aeat_simplified_invoice
            or super()._is_aeat_simplified_invoice()
        )
