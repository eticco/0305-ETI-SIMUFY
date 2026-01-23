from odoo import _, api, fields, models


class SaleWorkflowProcessEpt(models.Model):
    _inherit = "sale.workflow.process.ept"

    journal_amount_rule_ids = fields.One2many(
        "sale.journal.rule",
        "workflow_id",
        string="Reglas de Diario por Cantidad",
    )

    def get_journal_for_amount(self, amount, country_id):
        self.ensure_one()
        for rule in self.journal_amount_rule_ids:
            if rule.min_amount <= amount <= rule.max_amount:
                if (
                    (rule.region == "local" and country_id.code == "ES")
                    or (rule.region == "eu" and country_id.intrastat)
                    or (rule.region == "external" and not country_id.intrastat)
                ):
                    return rule.journal_id
        return None
