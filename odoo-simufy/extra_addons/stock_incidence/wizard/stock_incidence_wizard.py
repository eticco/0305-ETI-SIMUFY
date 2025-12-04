# -*- coding: utf-8 -*-
from odoo import api, models, fields


class StockIncidenceWizard(models.Model):
    _name = "stock.incidence.wizard"
    _description = "stock.incidence.wizard"

    picking_id = fields.Many2one(string="Albaran", comodel_name="stock.picking")
    incidence_id = fields.Many2one(
        string="Incidencia", comodel_name="stock.incidence", required=True
    )
    incidence_date = fields.Datetime(string="Fecha Registro Incidencia")

    def do_action(self):
        vals = {
            "incidence_id": self.incidence_id.id,
            "incidence_date": self.incidence_date or fields.datetime.now(),
        }
        self.picking_id.write(vals)  # contexto para saltar el bloqueo
        return True
