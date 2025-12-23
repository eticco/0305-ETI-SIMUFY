# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    import_dest_state_id = fields.Many2one(
        "res.country.state",
        string="Puerto Destino",
        ondelete="restrict",
        domain="[('country_id.code', '=', 'ES')]",
    )
    freight_forwarder_partner_id = fields.Many2one("res.partner", string="Transitario")

    is_origin_proforma = fields.Boolean(string="Proforma")
    is_origin_invoice = fields.Boolean(string="Factura")
    is_origin_delivery_note = fields.Boolean(string="Albarán")
    is_origin_bl = fields.Boolean(string="B/L")
    is_origin_telex = fields.Boolean(string="Telex")
    plastic_certificate = fields.Boolean(string="Certificado plástico")

    is_destiny_dua = fields.Boolean(string="DUA")
    is_destiny_dua_number = fields.Text(string="Número DUA")
    is_destiny_tax_invoice = fields.Boolean(string="Factura impuestos")
    is_destiny_forwarder_invoice = fields.Boolean(string="Factura transitario")
    is_destiny_external_transport_invoice = fields.Boolean(
        string="Factura transporte externo"
    )

    etd_date = fields.Date(string="ETD")
    port_eta_date = fields.Date(string="ETA (Puerto)")
    warehouse_eta_date = fields.Date(string="ETA (Almacén)")

    import_observations = fields.Text(string="Observaciones")

    destiny_warehouse_id = fields.Many2one("res.partner", string="Almacén de destino")
    destiny_transportation_id = fields.Many2one(
        "res.partner", string="Transporte en destino"
    )
    in_customs_warehouse = fields.Boolean(
        "Mercancía en depósito aduanero", default=False
    )

    freight_forwarder = fields.Char(string="Transitario")
    freight_forwarder_dispatch = fields.Boolean(string="Comunicado al transitario")
    freight_forwarder_quotation = fields.Boolean(string="Cotización del transitario")
    destiny_transportation = fields.Char(string="Transporte en destino")

    container_import_ids = fields.One2many(
        comodel_name="container.import",
        inverse_name="purchase_order_id",
        string="Contenedores",
    )

    # Propagamos fecha de importación a recepciones
    def write(self, vals):
        if vals.get("warehouse_eta_date", False):
            for picking_id in self.picking_ids:
                picking_id.with_context(write_wh_date=1).scheduled_date = vals[
                    "warehouse_eta_date"
                ]
            vals["date_planned"] = vals["warehouse_eta_date"]
        return super().write(vals)
