# -*- coding: utf-8 -*-
from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _set_scheduled_date(self):
        if self.env.context.get("write_wh_date", False):
            for picking in self:
                picking.move_lines.write({"date": picking.scheduled_date})
        else:
            super()._set_scheduled_date()
