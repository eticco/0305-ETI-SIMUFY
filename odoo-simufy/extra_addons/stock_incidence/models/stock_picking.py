# -*- coding: utf-8 -*-
from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    incidence_id = fields.Many2one(
        string="Incidencia",
        comodel_name="stock.incidence",
        ondelete="restrict",
        copy=False,
    )
    incidence_date = fields.Datetime(string="Fecha Registro Incidencia", copy=False)

    def action_delete_incidence(self):
        self.incidence_date = None
        self.incidence_id = None
