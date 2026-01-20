# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError, ValidationError


import logging

_logger = logging.getLogger(__name__)


class StockPickingSplitWizard(models.TransientModel):
    _name = "stock.picking.split.wizard"
    _description = "Modelo para dividir albaranes"

    name = fields.Char(string="nombre", default="/", compute="_compute_name")
    state = fields.Selection(
        string="Paso",
        selection=[("step1", "Seleccion Albaranes"), ("step2", "Seleccion Lineas")],
        default="step1",
    )
    picking_id = fields.Many2one(
        string="Albaran Base", comodel_name="stock.picking", readonly=True
    )
    ref_base = fields.Char(
        string="Referencia albaran Base", related="picking_id.client_order_ref"
    )
    picking_data_ids = fields.One2many(
        string="Cabecera Albaran",
        comodel_name="split.picking.data",
        inverse_name="wiz_id",
    )
    new_move_ids = fields.One2many(
        string="Lineas nuevas",
        comodel_name="new.picking.move.line",
        inverse_name="wiz_id",
    )
    move_ids = fields.One2many(
        string="Lineas Origen",
        comodel_name="split.picking.move.line",
        inverse_name="wiz_id",
    )

    @api.depends("picking_id")
    def _compute_name(self):
        for record in self:
            record.name = "Wizard {}".format(record.picking_id.name or "")

    @api.model
    def default_get(self, fields):
        res = super(StockPickingSplitWizard, self).default_get(fields)
        _logger.error(self.env.context)
        picking = self.env["stock.picking"].browse(self.env.context.get("active_id"))

        res.update(
            {
                "picking_id": picking.id,
                "picking_data_ids": [
                    (
                        0,
                        0,
                        {
                            "scheduled_date": picking.scheduled_date,
                            "ref": picking.client_order_ref,
                            "picking_id": picking.id,
                        },
                    )
                ],
                "move_ids": self.prepare_origin_line(picking),
            }
        )
        return res

    @api.onchange("new_move_ids")
    def _onchange_new_move_ids(self):
        for line in self.move_ids:
            origin_qty = self.get_product_origin_qty(self.picking_id, line.product_id)
            for new_line in self.new_move_ids.filtered(
                lambda l: l.product_id.id == line.product_id.id
            ):
                qty = new_line.product_uom._compute_quantity(
                    new_line.qty, line.product_uom, rounding_method="HALF-UP"
                )
                origin_qty -= qty
            line.sudo().write({"qty": origin_qty})

    @api.onchange("picking_data_ids")
    def _onchange_picking_data_ids(self):
        last = self.picking_data_ids[-1]
        if len(self.picking_data_ids.filtered(lambda l: l.ref == last.ref)) > 1:
            raise UserError("La referencia proveedor debe ser única!")

    def check_move_line_full_splitted(self):
        if self.move_ids.filtered(lambda l: l.state == "pending"):
            raise UserError(
                "Aún quedan cantidades en la lineas de origen sin asignar en un albarán!"
            )

    def next_step(self):
        self.state = "step2"
        return self.open_step_wizard()

    def return_back_step(self):
        self.state = "step1"
        return self.open_step_wizard()

    def open_step_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking.split.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "view_id": self.env.ref(
                "stock_picking_split.dspsolar_stock_picking_split_wizard_view"
            ).id,
            "target": "new",
        }

    def get_product_origin_qty(self, picking, product):
        qty = 0
        for line in picking.move_ids.filtered(lambda l: l.product_id.id == product.id):
            qty += line.product_uom._compute_quantity(
                line.product_uom_qty, product.uom_po_id, rounding_method="HALF-UP"
            )
        return qty

    def prepare_origin_line(self, picking):
        items = []
        for product in picking.move_ids.mapped("product_id"):
            items.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "qty": self.get_product_origin_qty(picking, product),
                        "product_uom": product.uom_po_id.id,
                    },
                )
            )
        return items

    def _picking_context(self):
        return dict()

    def create_pickings(self):
        # NOTE: Comentamos el chekeo de tener que asignar todas las cantidas en albaranes
        # self.check_move_line_full_splitted()
        self.picking_id.do_unreserve()

        for pick_data in self.picking_data_ids.filtered(lambda l: not l.picking_id):
            new_picking = self._create_split_backorder(
                self.picking_id,
                {
                    "scheduled_date": pick_data.scheduled_date,
                    "client_order_ref": pick_data.ref,
                },
            )
            new_moves = self.env["stock.move"]
            for new_moves_data in self.new_move_ids.filtered(
                lambda l: l.picking_data_id.id == pick_data.id
            ):
                move = self.picking_id.move_ids.filtered(
                    lambda l: l.product_id.id == new_moves_data.product_id.id
                    and l.product_uom_qty >= new_moves_data.qty
                )
                if move:
                    if (
                        float_is_zero(
                            new_moves_data.qty,
                            precision_rounding=move[0].product_id.uom_id.rounding,
                        )
                        or move[0].product_qty <= new_moves_data.qty
                    ):
                        # si el movimiento del albran base se pierde nos cargamos la operacion que tenga.
                        if move[0].move_ids:
                            move[0].move_ids.unlink()
                        # movemos el movimiento
                        move[0].write(
                            {
                                "picking_id": new_picking.id,
                                "date": pick_data.scheduled_date,
                                "date_deadline": pick_data.scheduled_date,
                                "product_uom_qty": new_moves_data.qty,
                            }
                        )
                    else:
                        new_move_vals = move[0]._split(new_moves_data.qty)
                        new_move = self.env["stock.move"].create(new_move_vals)
                        new_moves |= new_move

            if new_moves:
                new_moves.write(
                    {
                        "picking_id": new_picking.id,
                        "date_deadline": pick_data.scheduled_date,
                    }
                )

            picking_context = new_picking._picking_split_context()

            new_picking_vals = {"scheduled_date": pick_data.scheduled_date}
            if self.picking_id.is_locked:
                new_picking_vals["is_locked"] = True

            new_picking.with_context(picking_context).write(new_picking_vals)

        self.picking_id.action_assign()

        return True

    def _create_split_backorder(self, picking, default=None):
        self.ensure_one()
        picking_context = picking._picking_split_context()
        backorder_picking = picking.with_context(picking_context).copy(
            dict(
                {
                    "name": "/",
                    "move_ids": [],
                    "move_ids": [],
                    "backorder_id": picking.id,
                },
                **(default or {})
            )
        )
        picking.message_post(
            body=_(
                'El albarán <a href="#" '
                'data-oe-model="stock.picking" '
                'data-oe-id="%d">%s</a> ha sido creado.'
            )
            % (backorder_picking.id, backorder_picking.name),
            body_is_html=True,
        )
        return backorder_picking


class SplitPickingData(models.TransientModel):
    _name = "split.picking.data"
    _description = "Modelo para guardar los datos de la cab albaran"
    _rec_name = "ref"

    wiz_id = fields.Many2one(string="Wizard", comodel_name="stock.picking.split.wizard")
    picking_id = fields.Many2one(string="Albaran Origen", comodel_name="stock.picking")
    scheduled_date = fields.Datetime(
        string="Fecha Prevista", default=fields.datetime.now()
    )
    ref = fields.Char(string="Referencia Cliente / Proveedor")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "Albaran: {}".format(record.ref)))
        return result


class NewPickingMoveLine(models.TransientModel):
    _name = "new.picking.move.line"
    _description = "Modelo nuevas lineas"

    wiz_id = fields.Many2one(string="Wizard", comodel_name="stock.picking.split.wizard")
    picking_data_id = fields.Many2one(
        string="Albaran", comodel_name="split.picking.data", required=True
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    product_uom = fields.Many2one(
        comodel_name="uom.uom",
        string="Unidad de medida",
        domain="[('category_id', '=', product_uom_category_id)]",
    )
    product_uom_category_id = fields.Many2one(
        related="product_id.uom_po_id.category_id", readonly=True
    )
    qty = fields.Float(
        string="Cantidad", digits="Product Unit of Measure", default=0.0, required=True
    )
    allowed_product_ids = fields.Many2many(
        string="Filtro productos",
        comodel_name="product.product",
        compute="_compute_allowed_product_ids",
    )

    @api.depends("wiz_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            products = record.wiz_id.picking_id.move_ids.mapped("product_id")
            record.allowed_product_ids = products.ids

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if not self.product_uom:
            self.product_uom = self.product_id.uom_po_id.id


class SplitPickingMoveLine(models.TransientModel):
    _name = "split.picking.move.line"
    _description = "Modelo lineas del albaran base"

    wiz_id = fields.Many2one(string="Wizard", comodel_name="stock.picking.split.wizard")
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    product_uom = fields.Many2one(comodel_name="uom.uom", string="Unidad de medida")
    qty = fields.Float(
        string="Cantidad", digits="Product Unit of Measure", default=0.0, required=True
    )
    state = fields.Selection(
        string="estado",
        selection=[("done", "Dividido"), ("pending", "pendiente dividir")],
        default="pending",
        compute="_compute_state",
    )

    @api.depends("qty")
    def _compute_state(self):
        for record in self:
            if record.qty <= 0:
                record.state = "done"
            else:
                record.state = "pending"
