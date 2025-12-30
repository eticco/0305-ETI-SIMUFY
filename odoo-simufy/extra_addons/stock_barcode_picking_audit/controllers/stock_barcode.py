# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.stock_barcode.controllers.stock_barcode import StockBarcodeController

import logging

_logger = logging.getLogger(__name__)


class StockBarcodeController(StockBarcodeController):

    @http.route("/stock_barcode/get_barcode_data", type="json", auth="user")
    def get_barcode_data(self, model, res_id):
        request.session.prepare_from_barcode = True

        return super().get_barcode_data(model, res_id)
