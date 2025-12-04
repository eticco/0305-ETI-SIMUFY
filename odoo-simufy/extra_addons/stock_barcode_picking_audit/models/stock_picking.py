# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.osv import expression
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    user_prepared_by_ids = fields.Many2many(
        string="Preparado Por Usuario", comodel_name="res.users"
    )

    def write(self, vals):
        if self.env.context.get("from_barcode", False):
            vals.update(user_prepared_by_ids=[(4, self.env.uid)])

        return super(StockPicking, self).write(vals)
