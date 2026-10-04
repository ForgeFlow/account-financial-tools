from odoo import Command
from odoo.tests import TransactionCase


class TestAccountUsability(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = cls.env["account.account.tag"].create(
            {"name": "Test Tag", "applicability": "accounts"}
        )
        cls.account = cls.env["account.account"].create(
            {"name": "Test Account", "code": "1001"}
        )

    def test_accounting_groups(self):
        privilege = self.env.ref("account.res_groups_privilege_accounting")
        group_user = self.env.ref("account.group_account_user")
        group_readonly = self.env.ref("account.group_account_readonly")
        group_manager = self.env.ref("account.group_account_manager")
        # Full accounting groups are selectable in the user form
        self.assertEqual(group_user.privilege_id, privilege)
        self.assertEqual(group_readonly.privilege_id, privilege)
        # The accountant (manager) has the full accounting features
        self.assertIn(group_user, group_manager.all_implied_ids)

    def test_tag_accounts(self):
        # Accounts can be linked from the tag side
        self.tag.account_ids = [Command.link(self.account.id)]
        self.assertIn(self.tag, self.account.tag_ids)
        self.assertEqual(
            self.env["account.account"].search([("tag_ids", "in", self.tag.ids)]),
            self.account,
        )

    def test_settings(self):
        settings = self.env["res.config.settings"].create(
            {
                "anglo_saxon_accounting": True,
                "fiscalyear_last_day": 30,
                "fiscalyear_last_month": "6",
            }
        )
        settings.execute()
        company = self.env.company
        self.assertTrue(company.anglo_saxon_accounting)
        self.assertEqual(company.fiscalyear_last_day, 30)
        self.assertEqual(company.fiscalyear_last_month, "6")
