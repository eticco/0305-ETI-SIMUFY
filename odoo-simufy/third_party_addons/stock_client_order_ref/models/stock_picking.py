from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    client_order_ref = fields.Char(
        string="Referencia del cliente",
        copy=False,
        readonly=False,
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
    )


class StockMove(models.Model):
    _inherit = "stock.move"

    client_order_ref = fields.Char(string="Customer Reference", copy=False)

    def _prepare_procurement_values(self):
        """
        Adds the client order ref to the procurement values
        """

        res = super(StockMove, self)._prepare_procurement_values()
        res["client_order_ref"] = self.client_order_ref
        return res

    def _get_new_picking_values(self):
        """
        Gets the client order ref from the sale order in the procurement group
        """

        res = super(StockMove, self)._get_new_picking_values()
        if self.group_id and self.group_id.sale_id:
            res.update({"client_order_ref": self.group_id.sale_id.client_order_ref})
        return res
