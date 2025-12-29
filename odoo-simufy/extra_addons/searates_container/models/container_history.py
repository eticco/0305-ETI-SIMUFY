# -*- coding: utf-8 -*-
from odoo import _, models, api, fields


class ContainerHistory(models.Model):
    _name = "container.history"
    _description = "container.history"
    _order = "date desc"

    container_import_id = fields.Many2one(
        string="Contenedor", comodel_name="container.import"
    )

    location = fields.Char(string="Localización")
    date = fields.Datetime(string="Fecha")
    description = fields.Char(string="Descripción")
