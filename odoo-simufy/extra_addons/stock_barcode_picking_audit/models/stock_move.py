# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        if request.session.get("prepare_from_barcode", False):
            if self.picking_id:
                self.picking_id.user_prepared_by_ids = [(4, self.env.uid)]

        return super(StockMove, self).write(vals)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def write(self, vals):
        if request.session.get("prepare_from_barcode", False):
            if self.move_id and self.move_id.picking_id:
                self.move_id.picking_id.user_prepared_by_ids = [(4, self.env.uid)]

        return super(StockMoveLine, self).write(vals)
