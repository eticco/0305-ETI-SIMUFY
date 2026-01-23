from odoo import _, api, fields, models


class SaleJournalRule(models.Model):
    _name = "sale.journal.rule"
    _description = "Regla de Diario de Venta basada en Monto"

    workflow_id = fields.Many2one(
        "sale.workflow.process.ept",
        string="Flujo de Trabajo de Venta",
        required=True,
    )

    journal_id = fields.Many2one(
        "account.journal",
        string="Diario Contable",
        required=True,
        domain=[("type", "=", "sale")],
    )

    is_intracommunity = fields.Boolean(
        string="Intracomunitario",
        help="Indica si esta regla es para operaciones intracomunitarias.",
        default=False,
    )

    min_amount = fields.Float(
        string="Mínimo",
        required=True,
        help="Cantidad mínima para que esta regla se aplique.",
    )

    max_amount = fields.Float(
        string="Máximo",
        required=True,
        help="Cantidad máxima para que esta regla se aplique.",
    )

    @api.constrains("min_amount", "max_amount")
    def _check_amounts(self):
        for record in self:
            if record.min_amount < 0:
                raise ValueError(_("La cantidad mínima no puede ser negativa."))
            if record.max_amount <= record.min_amount:
                raise ValueError(
                    _("La cantidad máxima debe ser mayor que la cantidad mínima.")
                )

            overlapping_rules = self.search(
                [
                    ("workflow_id", "=", record.workflow_id.id),
                    ("is_intracommunity", "=", record.is_intracommunity),
                    ("id", "!=", record.id),
                    "|",
                    "&",
                    ("min_amount", "<=", record.min_amount),
                    ("max_amount", ">=", record.min_amount),
                    "&",
                    ("min_amount", "<=", record.max_amount),
                    ("max_amount", ">=", record.max_amount),
                ]
            )
            if overlapping_rules:
                raise ValueError(
                    _(
                        "Las cantidades definidas se solapan con otra regla en el mismo flujo de trabajo."
                    )
                )
