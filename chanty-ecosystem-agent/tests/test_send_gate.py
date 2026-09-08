"""The send gate. Nothing leaves unless every sub-gate passes."""

import copy
import datetime
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

    # A Tuesday at 10:00 in America/Chicago, so the send window is open and the
    # tests do not depend on what time it happens to be when they run.
    NOW = datetime.datetime(2026, 9, 8, 15, 0, tzinfo=datetime.timezone.utc)

    def _check(self, **kw):
        kw.setdefault("human_approved", True)
        kw.setdefault("now", self.NOW)
        return gates.check_send(self.org, self.contact, self.draft, self.opp,
                                root=self.root, **kw)

    def test_a_clean_human_approved_draft_passes_every_gate(self):
        result = self._check()
        self.assertTrue(result.passed, [f["check"] for f in result.failures])

    def test_compliance_passes_in_manual_gmail_draft_mode(self):
        result = gates.check_compliance_configured()
        self.assertTrue(result.passed, [f["check"] for f in result.failures])

    def test_no_postal_address_is_required_in_gmail_draft_mode(self):
        checks = [c["check"] for c in gates.check_compliance_configured().checks]
        self.assertNotIn("physical_address_set", checks)
        self.assertIn("opt_out_honored_on_reply", checks)

    def test_a_bulk_sending_mode_brings_the_requirements_back(self):
        """The mode decides, not the gate. Flip it and the gate tightens."""
        import json
        import tempfile
        from eco import policy
        cfg = json.loads(json.dumps(policy.load()))
        cfg["email_compliance"].update({
            "sending_mode": "bulk_platform",
            "physical_address_required": True,
            "opt_out_link_required": True,
            "opt_out_link_token": "{{unsubscribe_url}}",
        })
        path = tempfile.mkstemp(suffix=".json")[1]
        with open(path, "w") as fh:
            json.dump(cfg, fh)
        result = gates.check_compliance_configured(policy_path=path)
        self.assertFalse(result.passed)
        self.assertIn("physical_address_set", [f["check"] for f in result.failures])

        send = gates.check_send(self.org, self.contact, self.draft, self.opp,
                                root=self.root, policy_path=path, human_approved=True,
                                now=self.NOW)
        self.assertIn("opt_out_present", [f["check"] for f in send.failures])

    def test_a_sign_off_blocks(self):
        self.draft["body"] = self.draft["body"] + "\n\nBest,\nAustin"
        self.assertIn("format", [f["check"] for f in self._check().failures])

    def test_markdown_blocks(self):
        self.draft["body"] = self.draft["body"] + "\n\n- one\n- two"
        self.assertIn("format", [f["check"] for f in self._check().failures])

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
                                  root=self.root, human_approved=False, now=self.NOW)
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
