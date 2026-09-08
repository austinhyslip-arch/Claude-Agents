"""policy.md and policy.json must agree on the facts that matter."""

import re
import unittest

import helpers  # noqa: F401
from eco import paths, policy


def read(path):
    with open(path) as fh:
        return fh.read()


class PolicyConsistencyTest(unittest.TestCase):
    def setUp(self):
        self.md = read(paths.CONFIG_DIR + "/policy.md")

    def test_price_matches(self):
        self.assertIn("$3 per seat", self.md)
        self.assertEqual(policy.price_per_seat(), 3.0)

    def test_max_touches_matches(self):
        self.assertEqual(policy.max_touches(), 4)
        self.assertIn("Four touches maximum", self.md)

    def test_sequence_days_match(self):
        days = [t["day"] for t in policy.get("outreach_sequence")]
        self.assertEqual(days, [0, 4, 10, 21])
        self.assertIn("day 0, day 4, day 10, day 21", self.md)

    def test_enrichment_is_off_in_both(self):
        self.assertFalse(policy.enrichment_allowed())
        self.assertIn("No enrichment", self.md)

    def test_autonomy_level_matches(self):
        self.assertEqual(policy.autonomy_level(), 2)
        self.assertIn("Current level: **2**", self.md)

    def test_level_three_needs_the_first_twenty_reviewed(self):
        autonomy = policy.get("autonomy")
        self.assertEqual(autonomy["first_pilot_human_review_first_touch_count"], 20)
        self.assertEqual(autonomy["autonomous_send_enabled_categories"], [])
        self.assertIn("reviewed the first 20", autonomy["promotion_condition"])

    def test_no_discounts_are_configured(self):
        pricing = policy.get("chanty_pricing")
        for key in ("approved_discounts", "approved_commission_terms",
                    "approved_revenue_share_terms", "approved_exclusivity_terms",
                    "approved_free_account_terms", "approved_extended_trial_terms"):
            self.assertEqual(pricing[key], [], key)

    def test_sending_mode_is_manual_gmail_drafts(self):
        ec = policy.get("email_compliance")
        self.assertEqual(ec["sending_mode"], "manual_gmail_draft")
        self.assertEqual(ec["sending_infrastructure"], "gmail_draft_manual_send")
        self.assertEqual(ec["legal_review_status"], "reviewed")

    def test_bulk_mail_requirements_are_off_but_suppression_is_not(self):
        ec = policy.get("email_compliance")
        self.assertFalse(ec["physical_address_required"])
        self.assertFalse(ec["opt_out_link_required"])
        self.assertTrue(ec["opt_out_honored_on_reply"])
        self.assertTrue(ec["centralized_suppression_required"])
        self.assertEqual(ec["opt_out_processing_days_max"], 1)

    def test_email_format_is_plain_text_with_no_sign_off(self):
        fmt = policy.get("email_format")
        self.assertTrue(fmt["plain_text_only"])
        self.assertFalse(fmt["html_body_allowed"])
        self.assertFalse(fmt["markdown_allowed"])
        self.assertFalse(fmt["sign_off_allowed"])
        self.assertIn("Gmail", self.md)

    def test_scoring_bands_are_contiguous_and_cover_zero_to_hundred(self):
        bands = sorted(policy.get("scoring.bands"), key=lambda b: b["min"])
        self.assertEqual(bands[0]["min"], 0)
        self.assertEqual(bands[-1]["max"], 100)
        for a, b in zip(bands, bands[1:]):
            self.assertEqual(b["min"], a["max"] + 1)

    def test_every_approved_offer_appears_in_the_offer_library(self):
        offers = read(paths.CONFIG_DIR + "/offers.md").lower()
        for offer in policy.get("approved_offers"):
            words = offer.replace("_", " ")
            self.assertTrue(any(w in offers for w in words.split()), offer)

    def test_prohibited_phrases_are_documented(self):
        from eco import gates
        doc = read(paths.PROHIBITED_CLAIMS_FILE).lower()
        undocumented = [p for p in gates._PROHIBITED_PHRASES
                        if p.split()[0] not in doc]
        self.assertEqual(undocumented, [])

    def test_agent_permissions_deny_enrichment_for_every_agent_but_human(self):
        for agent, perms in policy.get("agent_permissions").items():
            if agent == "human":
                continue
            self.assertFalse(perms["may_use_enrichment"], agent)
            self.assertFalse(perms["may_send"], agent)
            self.assertFalse(perms["may_edit_policy"], agent)

    def test_learning_agent_locked_fields_match_the_module(self):
        from eco import learning
        self.assertEqual(set(policy.get("agent_permissions.learning.may_not_modify")),
                         learning.LOCKED)


class LearningGuardTest(unittest.TestCase):
    def test_locked_fields_raise(self):
        from eco import learning
        for field in learning.LOCKED:
            with self.assertRaises(learning.LockedFieldError):
                learning.guard(field)

    def test_allowed_fields_pass(self):
        from eco import learning
        for field in ("targeting", "scoring_weights", "offer_prioritization"):
            self.assertTrue(learning.guard(field))


if __name__ == "__main__":
    unittest.main()
