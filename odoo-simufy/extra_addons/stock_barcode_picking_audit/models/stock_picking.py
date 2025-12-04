# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.osv import expression
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    user_prepared_by_ids = fields.Many2many(
        string="Preparado Por Usuario", comodel_name="res.users"
    )

    def write(self, vals):
        if self.env.context.get("from_barcode", False):
            vals.update(user_prepared_by_ids=[(4, self.env.uid)])

        return super(StockPicking, self).write(vals)

    # @api.model
    # def read_group(
    #     self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    # ):

    #     if "employee_prepared_by_ids" not in groupby:
    #         return super().read_group(
    #             domain,
    #             fields,
    #             groupby,
    #             offset=offset,
    #             limit=limit,
    #             orderby=orderby,
    #             lazy=lazy,
    #         )
    #     res = []
    #     for employee in self.env["hr.employee"].search([]):
    #         count = self.env["stock.picking"].search_count(
    #             expression.AND(
    #                 [[("employee_prepared_by_ids", "ilike", employee.name)], domain]
    #             )
    #         )
    #         if not count:
    #             continue
    #         res.append(
    #             {
    #                 "__count": count,
    #                 "employee_prepared_by_ids": employee.name,
    #                 "employee_prepared_by_ids_count": count,
    #                 "__domain": expression.AND(
    #                     [domain, [("employee_prepared_by_ids", "ilike", employee.name)]]
    #                 ),
    #             }
    #         )

    #     count = self.env["stock.picking"].search_count(
    #         expression.AND([[("employee_prepared_by_ids", "=", False)], domain])
    #     )
    #     if count > 0:
    #         res.append(
    #             {
    #                 "__count": count,
    #                 "employee_prepared_by_ids": "Indefinido",
    #                 "employee_prepared_by_ids_count": count,
    #                 "__domain": expression.AND(
    #                     [domain, [("employee_prepared_by_ids", "=", False)]]
    #                 ),
    #             }
    #         )

    #     return res
