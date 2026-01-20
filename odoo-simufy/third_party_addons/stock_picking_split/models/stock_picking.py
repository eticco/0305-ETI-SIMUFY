from odoo import api, models, fields, _

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _picking_split_context(self):
        return dict(self.env.context).copy()
