"""Attribution keeps direct and assisted apart, and forecasts show their inputs."""

import copy
import unittest

import helpers
from eco import attribution


class AttributionTest(unittest.TestCase):
    def setUp(self):
        self.org = copy.deepcopy(helpers.ORG)

    def test_id_shape(self):
        rec = attribution.create(self.org, records=[])
        self.assertTrue(rec["attribution_id"].startswith("CHANTY-CHAMBER-"))
        self.assertTrue(rec["attribution_id"].endswith("-001"))

    def test_sequence_increments_within_a_type(self):
        first = attribution.create(self.org, records=[])
        second = attribution.create(self.org, records=[first])
        self.assertTrue(second["attribution_id"].endswith("-002"))

    def test_direct_and_assisted_are_separate(self):
        rec = attribution.create(self.org, records=[])
        attribution.add_outcome(rec, "direct", seats=40, paid_accounts=5)
        attribution.add_outcome(rec, "assisted", seats=12)
        self.assertEqual(rec["direct"]["seats"], 40)
        self.assertEqual(rec["assisted"]["seats"], 12)

    def test_unknown_metric_is_rejected(self):
        rec = attribution.create(self.org, records=[])
        with self.assertRaises(ValueError):
            attribution.add_outcome(rec, "direct", vibes=3)

    def test_unknown_bucket_is_rejected(self):
        rec = attribution.create(self.org, records=[])
        with self.assertRaises(ValueError):
            attribution.add_outcome(rec, "influenced", seats=1)

    def test_forecast_shows_its_inputs_and_says_they_are_assumptions(self):
        out = attribution.expected_paid_seats(900)
        self.assertEqual(out["basis"], "assumption")
        self.assertIn("trial_rate", out["inputs"])
        self.assertGreater(out["expected_paid_seats"], 0)

    def test_forecast_uses_policy_price(self):
        out = attribution.expected_paid_seats(900)
        self.assertAlmostEqual(out["expected_mrr"], out["expected_paid_seats"] * 3.0, places=2)

    def test_observed_rates_replace_assumptions_once_there_is_data(self):
        rec = attribution.create(self.org, records=[])
        attribution.add_outcome(rec, "direct", reach=1000, signups=30, activated_teams=12,
                                paid_accounts=6, seats=48)
        rates = attribution.observed_rates([rec])
        self.assertEqual(rates["source"], "observed")
        self.assertAlmostEqual(rates["trial_rate"], 0.03)
        self.assertAlmostEqual(rates["average_seats"], 8.0)

    def test_observed_rates_with_no_data_say_so(self):
        self.assertEqual(attribution.observed_rates([])["source"], "assumption")


if __name__ == "__main__":
    unittest.main()
