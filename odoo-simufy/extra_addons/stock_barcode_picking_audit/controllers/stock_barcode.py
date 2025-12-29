# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.stock_barcode.controllers.stock_barcode import StockBarcodeController

import logging

_logger = logging.getLogger(__name__)


class StockBarcodeController(StockBarcodeController):

    @http.route("/stock_barcode/scan_from_main_menu", type="json", auth="user")
    def main_menu(self, barcode, **kw):
        context = dict(request.env.context)
        context.update(from_barcode=True)
        request.env.context = context

        return super().main_menu(barcode, **kw)
