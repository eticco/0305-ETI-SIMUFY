from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def write(self, vals):
        old_states = {}
        for rec in self:
            old_states[rec.id] = rec.delivery_state

        res = super().write(vals)

        current_delivery_state = vals.get("delivery_state", False)
        if current_delivery_state:
            for rec in self:
                if old_states.get(rec.id) != current_delivery_state:
                    if (
                        rec.carrier_id.whatsapp_template_id
                        and current_delivery_state
                        in rec.carrier_id.whatsapp_notify_state_ids.mapped("name")
                    ):
                        template = rec.carrier_id.whatsapp_template_id

                        self.env["whatsapp.composer"].new(
                            {
                                "res_ids": [rec.id],
                                "res_model": "stock.picking",
                                "wa_template_id": template.id,
                            }
                        ).action_send_whatsapp_template()

        return res

    @api.model
    def cron_update_delivery_states(self):
        pickings = self.env["stock.picking"].search(
            [
                ("state", "=", "done"),
                (
                    "delivery_state",
                    "not in",
                    ["customer_delivered", "canceled_shipment", "no_update"],
                ),
                ("delivery_type", "not in", [False, "fixed", "base_one_rule"]),
                ("delivery_type.whatsapp_template_id", "!=", False),
            ]
        )

        pickings._update_delivery_state()
