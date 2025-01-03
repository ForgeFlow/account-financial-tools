# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    restrict_mode_hash_table = fields.Boolean(
        compute="_compute_restrict_mode_hash_table", store=True, readonly=True
    )

    @api.constrains("restrict_mode_hash_table", "type")
    def _check_journal_restrict_mode(self):
        for rec in self:
            if not rec.restrict_mode_hash_table and rec.type in [
                "sale",
                "purchase",
                "general",
            ]:
                raise UserError(
                    _("Journal %s must have Lock Posted Entries enabled.") % rec.name
                )

    @api.depends("type")
    def _compute_restrict_mode_hash_table(self):
        for rec in self:
            rec.restrict_mode_hash_table = rec.type in ["sale", "purchase", "general"]
