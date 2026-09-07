"""Responses stop automation and route to humans."""

import unittest

import helpers  # noqa: F401  (path setup)
from eco import response


class ResponseTest(unittest.TestCase):
    def test_positive_stops_automation(self):
        plan = response.plan("POSITIVE")
        self.assertTrue(plan["stop_automation"])
        self.assertEqual(plan["next_event"], "escalate")

    def test_every_class_except_ooo_stops_automation(self):
        for c in response.CLASSES:
            self.assertEqual(response.stops_automation(c), c != "OOO", c)

    def test_pricing_routes_to_a_human(self):
        plan = response.plan("PRICING", "What would this cost our members?")
        self.assertTrue(plan["escalate"])
        self.assertTrue(plan["stop_automation"])

    def test_pricing_question_inside_a_neutral_reply_still_escalates(self):
        plan = response.plan("NEUTRAL", "Interesting. How much is it per seat?")
        self.assertTrue(plan["escalate"])

    def test_commission_question_escalates(self):
        self.assertTrue(response.plan("NEUTRAL", "Is there a commission for referrals?")["escalate"])

    def test_security_and_hipaa_escalate(self):
        self.assertTrue(response.plan("NEUTRAL", "Do you have SOC 2?")["escalate"])
        self.assertTrue(response.plan("NEUTRAL", "Are you HIPAA compliant?")["escalate"])

    def test_opt_out_writes_suppression(self):
        for body in ("Please remove me from your list", "unsubscribe", "do not contact me again"):
            plan = response.plan("NEGATIVE", body)
            self.assertTrue(plan["suppress"], body)
            self.assertEqual(plan["next_event"], "suppress")

    def test_plain_no_thanks_goes_to_nurture_not_suppression(self):
        plan = response.plan("NEGATIVE", "Not a fit for us right now, thanks.")
        self.assertFalse(plan["suppress"])
        self.assertEqual(plan["next_event"], "nurture")

    def test_unknown_classification_raises(self):
        with self.assertRaises(ValueError):
            response.plan("MAYBE_LATER")


if __name__ == "__main__":
    unittest.main()
