"""Claims, pricing and evidence."""

import copy
import unittest

import helpers
from eco import gates, policy


class PricingTest(unittest.TestCase):
    def test_discount_language_fails(self):
        for text in ("We can offer your members a 20% discount",
                     "special pricing for chamber members",
                     "a reduced rate for your community",
                     "free accounts for the first 50 members",
                     "we'd give you an extended trial"):
            self.assertFalse(gates.check_claims(text).passed, text)

    def test_commission_and_revshare_language_fails(self):
        for text in ("we pay a 20% commission on referrals",
                     "happy to talk rev share",
                     "there's a referral fee for partners",
                     "we could make this an exclusive partnership"):
            self.assertFalse(gates.check_claims(text).passed, text)

    def test_correct_price_passes(self):
        self.assertTrue(gates.check_claims("Chanty is $3 per seat.").passed)

    def test_any_other_price_fails(self):
        for text in ("Chanty is $2 per seat for members", "normally $5 per seat"):
            result = gates.check_claims(text)
            self.assertFalse(result.passed, text)
            self.assertIn("no_unauthorized_price", [f["check"] for f in result.failures])

    def test_policy_price_is_three_dollars(self):
        self.assertEqual(policy.price_per_seat(), 3.0)


class FabricationTest(unittest.TestCase):
    def test_fake_urgency_fails(self):
        for text in ("limited spots available", "this month only", "last chance to book"):
            self.assertFalse(gates.check_claims(text).passed, text)

    def test_generic_flattery_fails(self):
        self.assertFalse(gates.check_claims("Big fan of what you're doing over there").passed)

    def test_regulated_topics_fail(self):
        for text in ("we are HIPAA compliant", "we have SOC 2 Type II", "GDPR is covered"):
            self.assertFalse(gates.check_claims(text).passed, text)


class EvidenceTest(unittest.TestCase):
    def test_a_message_with_no_evidence_fails(self):
        result = gates.check_personalization("I noticed you run monthly workshops.", [])
        self.assertFalse(result.passed)
        self.assertIn("has_evidence", [f["check"] for f in result.failures])

    def test_D_level_evidence_cannot_support_a_message(self):
        result = gates.check_personalization(
            "I noticed you run monthly workshops.",
            [{"claim": "runs monthly workshops", "source_type": "D",
              "source_url": "https://search.test/result", "confidence": "ESTIMATE"}])
        self.assertFalse(result.passed)
        self.assertIn("no_D_level_evidence", [f["check"] for f in result.failures])

    def test_claim_without_a_source_url_fails(self):
        result = gates.check_personalization(
            "I noticed you run monthly workshops.",
            [{"claim": "runs monthly workshops", "source_type": "A", "source_url": None}])
        self.assertFalse(result.passed)
        self.assertIn("every_claim_has_source_url", [f["check"] for f in result.failures])

    def test_estimate_stated_as_a_bare_number_fails(self):
        result = gates.check_personalization(
            "Your 2,500 members would find this useful.",
            [{"claim": "roughly 2,500 member businesses", "source_type": "C",
              "source_url": "https://third-party.test/profile", "confidence": "ESTIMATE"}])
        self.assertFalse(result.passed)
        self.assertIn("no_estimate_stated_as_fact", [f["check"] for f in result.failures])

    def test_same_estimate_phrased_without_the_number_passes(self):
        result = gates.check_personalization(
            "Your member community would find this useful.",
            [{"claim": "roughly 2,500 member businesses", "source_type": "C",
              "source_url": "https://third-party.test/profile", "confidence": "ESTIMATE"}])
        self.assertTrue(result.passed, result.failures)

    def test_the_good_draft_passes_both_gates(self):
        draft = copy.deepcopy(helpers.DRAFT)
        body = draft["subject"] + "\n" + draft["body"]
        self.assertTrue(gates.check_claims(body).passed)
        self.assertTrue(gates.check_personalization(body, draft["personalization_claims"]).passed)


if __name__ == "__main__":
    unittest.main()
