from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        if self.auto_workflow_process_id:
            journal_id = self.auto_workflow_process_id.get_journal_for_amount(
                self.amount_total, self.partner_id.country_id
            )
            if journal_id:
                invoice_vals.update({"journal_id": journal_id.id})

        return invoice_vals
