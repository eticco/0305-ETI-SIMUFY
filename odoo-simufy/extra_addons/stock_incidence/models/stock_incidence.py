# -*- coding: utf-8 -*-

from odoo import api, models, fields


class StockIncidence(models.Model):
    _name = "stock.incidence"
    _description = "stock.incidence"

    active = fields.Boolean(string="Activo", default=True)
    name = fields.Char(string="Nombre")
