"""A suppressed contact must not reach the send queue through any path."""

import copy
import unittest

import helpers
from eco import gates, store


class SuppressionTest(unittest.TestCase):
    def setUp(self):
        self.root = helpers.temp_root()
        helpers.silence_audit(self)
        self.org = copy.deepcopy(helpers.ORG)
        self.contact = copy.deepcopy(helpers.CONTACT)
        store.put("organizations", self.org, root=self.root, log=False)
        store.put("contacts", self.contact, root=self.root, log=False)
        store.put("opportunities", copy.deepcopy(helpers.OPPORTUNITY), root=self.root, log=False)

    def _suppress(self, scope, value, reason="requested_no_contact"):
        store.put("suppression", {
            "suppression_id": "SUP-TESTAA01", "scope": scope, "value": value,
            "reason": reason, "permanent": True, "created_at": "2026-09-01T00:00:00+00:00",
            "created_by": "human", "note": None, "lifted_at": None, "lifted_by": None,
        }, root=self.root, log=False)

    def test_contact_scope_blocks_send(self):
        self._suppress("contact", self.contact["contact_id"])
        result = gates.check_send(self.org, self.contact, helpers.DRAFT,
                                  helpers.OPPORTUNITY, root=self.root, human_approved=True)
        self.assertFalse(result.passed)
        self.assertIn("suppression", [f["check"] for f in result.failures])

    def test_email_scope_blocks_send(self):
        self._suppress("contact", self.contact["email"])
        self.assertFalse(gates.check_suppression(self.org, self.contact, root=self.root).passed)

    def test_organization_scope_blocks_every_contact(self):
        self._suppress("organization", self.org["organization_id"], "complaint")
        self.assertFalse(gates.check_suppression(self.org, self.contact, root=self.root).passed)

    def test_domain_scope_blocks_send(self):
        self._suppress("domain", "example-valley-chamber.test", "unsubscribed")
        self.assertFalse(gates.check_suppression(self.org, self.contact, root=self.root).passed)

    def test_suppression_also_blocks_the_qualification_gate(self):
        self._suppress("organization", self.org["organization_id"])
        result = gates.check_qualification(self.org, self.contact, helpers.OPPORTUNITY,
                                           root=self.root)
        self.assertFalse(result.passed)
        self.assertIn("no_suppression", [f["check"] for f in result.failures])

    def test_lifted_suppression_no_longer_blocks(self):
        store.put("suppression", {
            "suppression_id": "SUP-TESTAA02", "scope": "contact",
            "value": self.contact["contact_id"], "reason": "manual", "permanent": False,
            "created_at": "2026-09-01T00:00:00+00:00", "created_by": "human",
            "note": "lifted by Austin", "lifted_at": "2026-09-05T00:00:00+00:00",
            "lifted_by": "human",
        }, root=self.root, log=False)
        self.assertTrue(gates.check_suppression(self.org, self.contact, root=self.root).passed)

    def test_contact_flag_alone_blocks(self):
        c = dict(self.contact, suppressed=True)
        self.assertFalse(gates.check_suppression(self.org, c, root=self.root).passed)


if __name__ == "__main__":
    unittest.main()
