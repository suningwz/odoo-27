# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
 #Se realiza traduccion al español realizado por Brandon Martin
ACCOUNT_STAGES = [
    ("draft", "Borrador"),
    ("review", "Revisión de Necesidades"),
    ("confirmed", "Confirmado"),
    ("invoiced", "Facturado"),
    ("nothing Invoiced", "Nada Facturado"),
]


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    contractor_cost_ids = fields.One2many(
        "fsm.order.cost", "fsm_order_id", string="Productos a Facturar"
    )
    employee_timesheet_ids = fields.One2many(
        "account.analytic.line", "fsm_order_id", string="Horas Trabajadas por el Empleado"
    )
    employee = fields.Boolean(compute="_compute_employee")
    contractor_total = fields.Float(
        compute="_compute_contractor_cost", string="Costo Total"
    )
    employee_time_total = fields.Float(
        compute="_compute_employee_hours", string="Hora Total del Empleado"
    )
    account_stage = fields.Selection(
        ACCOUNT_STAGES, string="Accounting Stage", default="draft"
    )

    def _compute_employee(self):
        user = self.env["res.users"].browse(self.env.uid)
        for order in self:
            if user.employee_ids:
                order.employee = True
            else:
                order.employee = False

    @api.depends("employee_timesheet_ids", "contractor_cost_ids")
    def _compute_total_cost(self):
        super()._compute_total_cost()
        for order in self:
            order.total_cost = 0.0
            rate = 0
            for line in order.employee_timesheet_ids:
                rate = line.employee_id.timesheet_cost
                order.total_cost += line.unit_amount * rate
            for cost in order.contractor_cost_ids:
                order.total_cost += cost.price_unit * cost.quantity

    @api.depends("employee_timesheet_ids")
    def _compute_employee_hours(self):
        for order in self:
            order.employee_time_total = 0.0
            for line in order.employee_timesheet_ids:
                order.employee_time_total += line.unit_amount

    @api.depends("contractor_cost_ids")
    def _compute_contractor_cost(self):
        for order in self:
            order.contractor_total = 0.0
            for cost in order.contractor_cost_ids:
                order.contractor_total += cost.price_unit * cost.quantity

    def action_complete(self):
        for order in self:
            order.account_stage = "review"
        if self.person_id.supplier_rank and not self.contractor_cost_ids:
            raise ValidationError(
                _("No se puede mover a Completar" + "hasta que se complete 'Productos a Facturar")
            )
        if not self.person_id.supplier_rank and not self.employee_timesheet_ids:
            raise ValidationError(
                _(
                    "Verificar por favor en el modulo de Pre-Factura/Horas trabajadas por el empleado que los "
                    "campos esten completos"
                )
            )
        return super(FSMOrder, self).action_complete()

    def create_bills(self):
        jrnl = self.env["account.journal"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("type", "=", "purchase"),
                ("active", "=", True),
            ],
            limit=1,
        )
        fpos = self.person_id.partner_id.property_account_position_id
        invoice_line_vals = []
        for cost in self.contractor_cost_ids:
            template = cost.product_id.product_tmpl_id
            accounts = template.get_product_accounts()
            account = accounts["expense"]
            taxes = template.supplier_taxes_id
            tax_ids = fpos.map_tax(taxes)
            invoice_line_vals.append(
                (
                    0,
                    0,
                    {
                        "analytic_account_id": self.location_id.analytic_account_id.id,
                        "product_id": cost.product_id.id,
                        "quantity": cost.quantity,
                        "name": cost.product_id.display_name,
                        "price_unit": cost.price_unit,
                        "account_id": account.id,
                        "fsm_order_ids": [(4, self.id)],
                        "tax_ids": [(6, 0, tax_ids.ids)],
                    },
                )
            )
        vals = {
            "partner_id": self.person_id.partner_id.id,
            "move_type": "in_invoice",
            "journal_id": jrnl.id or False,
            "fiscal_position_id": fpos.id or False,
            "fsm_order_ids": [(4, self.id)],
            "company_id": self.env.company.id,
            "invoice_line_ids": invoice_line_vals,
        }
        bill = self.env["account.move"].sudo().create(vals)
        bill._recompute_tax_lines()

    def account_confirm(self):
        for order in self:
            contractor = order.person_id.partner_id.supplier_rank
            if order.contractor_cost_ids:
                if contractor:
                    order.create_bills()
                    order.account_stage = "confirmed"
                else:
                    raise ValidationError(
                        _("El trabajador asignado a este pedido no es un proveedor")
                    )
            if order.employee_timesheet_ids:
                order.account_stage = "confirmed"

    def account_create_invoice(self):
        jrnl = self.env["account.journal"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("type", "=", "sale"),
                ("active", "=", True),
            ],
            limit=1,
        )
        if self.bill_to == "contact":
            if not self.customer_id:
                raise ValidationError(_("Customer empty"))
            fpos = self.customer_id.property_account_position_id
            invoice_vals = {
                "partner_id": self.customer_id.id,
                "move_type": "out_invoice",
                "journal_id": jrnl.id or False,
                "fiscal_position_id": fpos.id or False,
                "fsm_order_ids": [(4, self.id)],
            }
            price_list = self.customer_id.property_product_pricelist

        else:
            fpos = self.location_id.customer_id.property_account_position_id
            invoice_vals = {
                "partner_id": self.location_id.customer_id.id,
                "move_type": "out_invoice",
                "journal_id": jrnl.id or False,
                "fiscal_position_id": fpos.id or False,
                "fsm_order_ids": [(4, self.id)],
                "company_id": self.env.company.id,
            }
            price_list = self.location_id.customer_id.property_product_pricelist

        invoice_line_vals = []
        for cost in self.contractor_cost_ids:
            price = price_list.get_product_price(
                product=cost.product_id,
                quantity=cost.quantity,
                partner=invoice_vals.get("partner_id"),
                date=False,
                uom_id=False,
            )
            template = cost.product_id.product_tmpl_id
            accounts = template.get_product_accounts()
            account = accounts["income"]
            taxes = template.taxes_id
            tax_ids = fpos.map_tax(taxes)
            invoice_line_vals.append(
                (
                    0,
                    0,
                    {
                        "product_id": cost.product_id.id,
                        "analytic_account_id": self.location_id.analytic_account_id.id,
                        "quantity": cost.quantity,
                        "name": cost.product_id.display_name,
                        "price_unit": price,
                        "account_id": account.id,
                        "fsm_order_ids": [(4, self.id)],
                        "tax_ids": [(6, 0, tax_ids.ids)],
                    },
                )
            )
        for line in self.employee_timesheet_ids:
            price = price_list.get_product_price(
                product=line.product_id,
                quantity=line.unit_amount,
                partner=invoice_vals.get("partner_id"),
                date=False,
                uom_id=False,
            )
            template = line.product_id.product_tmpl_id
            accounts = template.get_product_accounts()
            account = accounts["income"]
            taxes = template.taxes_id
            tax_ids = fpos.map_tax(taxes)
            invoice_line_vals.append(
                (
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "analytic_account_id": line.account_id.id,
                        "quantity": line.unit_amount,
                        "name": line.name,
                        "price_unit": price,
                        "account_id": account.id,
                        "fsm_order_ids": [(4, self.id)],
                        "tax_ids": [(6, 0, tax_ids.ids)],
                    },
                )
            )

        invoice_vals.update({"invoice_line_ids": invoice_line_vals})
        invoice = self.env["account.move"].sudo().create(invoice_vals)

        invoice._recompute_tax_lines()
        self.account_stage = "invoiced"
        return invoice

    def account_no_invoice(self):
        self.account_stage = "no"
