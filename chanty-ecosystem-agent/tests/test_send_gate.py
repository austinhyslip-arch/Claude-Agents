"""The send gate. Nothing leaves unless every sub-gate passes."""

import copy
import unittest

import helpers
from eco import gates, store


class SendGateTest(unittest.TestCase):
    def setUp(self):
        self.root = helpers.temp_root()
        helpers.silence_audit(self)
        self.org = copy.deepcopy(helpers.ORG)
        self.contact = copy.deepcopy(helpers.CONTACT)
        self.opp = copy.deepcopy(helpers.OPPORTUNITY)
        self.draft = copy.deepcopy(helpers.DRAFT)
        for coll, rec in (("organizations", self.org), ("contacts", self.contact),
                          ("opportunities", self.opp)):
            store.put(coll, rec, root=self.root, log=False)

    def _check(self, **kw):
        kw.setdefault("human_approved", True)
        return gates.check_send(self.org, self.contact, self.draft, self.opp,
                                root=self.root, **kw)

    def test_blocked_by_compliance_config_out_of_the_box(self):
        result = gates.check_send(self.org, self.contact, self.draft, self.opp,
                                  root=self.root, human_approved=True)
        self.assertFalse(result.passed)
        self.assertIn("email_compliance", [f["check"] for f in result.failures])

    def test_compliance_is_the_only_thing_blocking_a_clean_draft(self):
        result = self._check()
        self.assertEqual([f["check"] for f in result.failures], ["email_compliance"])

    def test_missing_opt_out_token_blocks(self):
        self.draft["body"] = self.draft["body"].replace("{{unsubscribe_url}}", "")
        self.assertIn("opt_out_present", [f["check"] for f in self._check().failures])

    def test_unapproved_offer_blocks(self):
        self.draft["offer"] = "free_pilot_program"
        self.assertIn("offer_approved", [f["check"] for f in self._check().failures])

    def test_contact_without_public_email_blocks(self):
        self.contact.update({"email_status": "not_publicly_found", "email": None,
                             "requires_user_permission": True})
        failures = [f["check"] for f in self._check().failures]
        self.assertIn("email_publicly_available", failures)

    def test_no_human_approval_at_level_zero_blocks(self):
        result = gates.check_send(self.org, self.contact, self.draft, self.opp,
                                  root=self.root, human_approved=False)
        self.assertIn("autonomy_or_human_approval", [f["check"] for f in result.failures])

    def test_a_reply_already_received_blocks_further_touches(self):
        store.put("outreach", dict(self.draft, outreach_id="OUT-TESTAA02", status="sent",
                                   sent_at="2026-08-01T00:00:00+00:00",
                                   response_classification="POSITIVE"),
                  root=self.root, log=False)
        self.assertIn("recent_outreach", [f["check"] for f in self._check().failures])

    def test_max_touches_is_enforced(self):
        for i in range(4):
            store.put("outreach", dict(self.draft, outreach_id="OUT-TESTAB0%d" % i,
                                       touch_number=i + 1, status="sent",
                                       sent_at="2026-07-0%dT00:00:00+00:00" % (i + 1)),
                      root=self.root, log=False)
        result = self._check()
        self.assertIn("recent_outreach", [f["check"] for f in result.failures])

    def test_pending_escalation_blocks(self):
        self.opp["escalation_required"] = True
        self.assertIn("no_pending_escalation", [f["check"] for f in self._check().failures])

    def test_sub_results_are_reported_for_debugging(self):
        result = self._check()
        self.assertIn("hard_qualification", result.sub_results)
        self.assertIn("claims", result.sub_results)


class QualificationGateTest(unittest.TestCase):
    def setUp(self):
        self.root = helpers.temp_root()
        helpers.silence_audit(self)
        self.org = copy.deepcopy(helpers.ORG)
        self.contact = copy.deepcopy(helpers.CONTACT)
        self.opp = copy.deepcopy(helpers.OPPORTUNITY)

    def _g(self):
        return gates.check_qualification(self.org, self.contact, self.opp, root=self.root)

    def test_the_good_record_passes(self):
        self.assertTrue(self._g().passed, self._g().failures)

    def test_unverified_organization_fails(self):
        self.org["status"] = "unverified"
        self.assertIn("organization_verified", [f["check"] for f in self._g().failures])

    def test_no_distribution_mechanism_fails(self):
        self.org["distribution"] = {}
        self.assertIn("distribution_mechanism_identified", [f["check"] for f in self._g().failures])

    def test_thin_evidence_fails(self):
        self.org["evidence"] = self.org["evidence"][:1]
        self.assertIn("evidence_exists", [f["check"] for f in self._g().failures])

    def test_only_D_level_evidence_fails(self):
        for e in self.org["evidence"]:
            e["source_type"] = "D"
        self.assertIn("evidence_exists", [f["check"] for f in self._g().failures])

    def test_missing_contact_fails(self):
        self.contact = None
        self.assertIn("credible_contact_identified", [f["check"] for f in self._g().failures])

    def test_no_partnership_hypothesis_fails(self):
        self.opp["why_this_offer"] = None
        self.assertIn("partnership_hypothesis_exists", [f["check"] for f in self._g().failures])

    def test_unresolved_contradiction_fails(self):
        self.org["contradictions"] = ["website says 900 members, LinkedIn says 4,000"]
        self.assertIn("no_material_contradiction", [f["check"] for f in self._g().failures])


if __name__ == "__main__":
    unittest.main()
