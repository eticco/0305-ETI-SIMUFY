from odoo import _, api, fields, models


DELIVERY_STATE = {
    "shipping_recorded_in_carrier": "Envío registrado en el transportista",
    "in_transit": "En tránsito",
    "canceled_shipment": "Envío cancelado",
    "incident": "Incidente",
    "customer_delivered": "Entregado al cliente",
    "warehouse_delivered": "Entregado en almacén",
    "no_update": "No hay más actualizaciones del transportista",
}


class WhatsappNotifyState(models.Model):
    _name = "whatsapp.notify.state"
    _rec_name = "complete_name"

    name = fields.Char("State", required=True)

    complete_name = fields.Char(
        "Complete Name",
        compute="_compute_complete_name",
        recursive=True,
        store=True,
    )

    @api.depends("name")
    def _compute_complete_name(self):
        for record in self:
            record.complete_name = DELIVERY_STATE.get(record.name)


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    whatsapp_template_id = fields.Many2one(
        comodel_name="whatsapp.template",
        string="WhatsApp Template",
        domain="[('model', '=', 'stock.picking')]",
    )

    whatsapp_notify_state_ids = fields.Many2many(
        comodel_name="whatsapp.notify.state",
        string="Estados de notificación por WhatsApp",
    )
