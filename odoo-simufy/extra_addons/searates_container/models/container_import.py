# -*- coding: utf-8 -*-
from odoo import _, models, api, fields
import requests
import json

import logging

_logger = logging.getLogger(__name__)


class ContainerImport(models.Model):
    _name = "container.import"
    _description = "container.import"

    purchase_order_id = fields.Many2one(
        string="Pedido de compra", comodel_name="purchase.order"
    )

    searates_active_sync = fields.Boolean(
        string="Sincronizar con Searates",
        compute="_compute_searates_active_sync",
        store=True,
    )

    ref = fields.Char(string="Referencia")

    json_return = fields.Text(string="JSON Searates")
    sealine_name = fields.Char(
        string="Naviera", compute="_compute_searates", store=True
    )
    status = fields.Char(string="Estado", compute="_compute_searates", store=True)
    updated_at = fields.Datetime(
        string="Actualizado", compute="_compute_searates", store=True
    )
    vessel_name = fields.Char(string="Buque", compute="_compute_searates", store=True)

    container_history_ids = fields.One2many(
        string="Historial",
        comodel_name="container.history",
        inverse_name="container_import_id",
        compute="_compute_searates",
        store=True,
    )

    @api.depends("purchase_order_id.picking_ids.state")
    def _compute_searates_active_sync(self):
        for container in self:
            container.searates_active_sync = any(
                container.purchase_order_id.picking_ids.filtered(
                    lambda p: p.state not in ["done", "cancel"]
                )
            )

    @api.depends("json_return")
    def _compute_searates(self):
        for container in self:
            if container.json_return:
                data = json.loads(container.json_return)

                if "status" in data and data["status"] == "success":
                    if "data" in data:
                        if "metadata" in data["data"]:
                            container.sealine_name = data["data"]["metadata"][
                                "sealine_name"
                            ]
                            container.status = data["data"]["metadata"]["status"]
                            container.updated_at = data["data"]["metadata"][
                                "updated_at"
                            ]

                        if (
                            "vessels" in data["data"]
                            and len(data["data"]["vessels"]) > 0
                        ):
                            container.vessel_name = data["data"]["vessels"][0]["name"]

                        if (
                            "containers" in data["data"]
                            and len(data["data"]["containers"]) > 0
                        ):
                            if "events" in data["data"]["containers"][0]:
                                container.container_history_ids.unlink()
                                for history in data["data"]["containers"][0]["events"]:
                                    location = [
                                        loc
                                        for loc in data["data"]["locations"]
                                        if loc["id"] == history["location"]
                                    ]

                                    container.container_history_ids = [
                                        (
                                            0,
                                            0,
                                            {
                                                "container_import_id": container.id,
                                                "location": "%s, %s, %s"
                                                % (
                                                    location[0]["name"],
                                                    location[0]["state"],
                                                    location[0]["country"],
                                                ),
                                                "date": history["date"],
                                                "description": history["description"],
                                            },
                                        )
                                    ]

    def get_container_json(self):
        self.ensure_one()

        searates_endpoint = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("searates_container.searates_endpoint")
        )
        searates_api_key = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("searates_container.searates_api_key")
        )

        if self.ref:
            parameters = dict(
                api_key=searates_api_key,
                number=self.ref,
                type="CT",
            )

            resp = requests.get(
                url="%s/tracking" % searates_endpoint, params=parameters
            )
            if resp.status_code == 200:
                self.json_return = resp.content

    def cron_action_update_searates(self):
        for container in self.search([("searates_active_sync", "=", True)]):
            container.get_container_json()
