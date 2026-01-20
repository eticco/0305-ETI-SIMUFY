from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        """
        Adds the client order ref to the procurement values passed to create a stock picking
        """
        self.ensure_one()
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({"client_order_ref": self.order_id.client_order_ref})
        return values
