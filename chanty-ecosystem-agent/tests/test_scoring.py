"""Scoring behaves the same way every time, and unresearched means zero."""

import unittest

import helpers  # noqa: F401
from eco import scoring


FULL = {
    "audience_fit": {"smb_concentration": 5, "employee_size_fit": 4,
                     "team_communication_need": 4, "vertical_relevance": 3,
                     "geographic_reach": 2},
    "distribution_power": {"email_newsletter": 5, "webinars_workshops": 3, "events": 4,
                           "member_client_communication": 4,
                           "community_directory_repeat_exposure": 3},
    "partnership_compatibility": {"technology_sponsors": 3, "member_benefits": 4,
                                  "educational_partnerships": 4, "referral_structure": 2},
    "timing": {"upcoming_event": 4, "current_initiative": 2,
               "leadership_or_program_change": 0},
    "strategic_value": {"multi_chapter_national_leverage": 1, "potential_seat_volume": 3,
                        "lookalike_potential": 4},
}


class ScoringTest(unittest.TestCase):
    def test_perfect_scores_one_hundred(self):
        perfect = {dim: {c: 5 for c in spec["components"]}
                   for dim, spec in scoring.DIMENSIONS.items()}
        result = scoring.score(perfect)
        self.assertEqual(result["organization_score"], 100.0)
        self.assertEqual(result["priority_band"], "STRATEGIC")

    def test_empty_scores_zero_and_archives(self):
        result = scoring.score({})
        self.assertEqual(result["organization_score"], 0.0)
        self.assertEqual(result["priority_band"], "ARCHIVE")
        self.assertEqual(result["coverage"], 0.0)

    def test_deterministic(self):
        self.assertEqual(scoring.score(FULL), scoring.score(FULL))

    def test_bands_line_up_with_policy(self):
        cases = [(95, "STRATEGIC"), (85, "TIER_1"), (70, "TIER_2"), (55, "NURTURE"), (20, "ARCHIVE")]
        for value, band in cases:
            scaled = {"audience_fit": {"smb_concentration": 5}}
            del scaled
            from eco import policy
            self.assertEqual(policy.band_for_score(value), band)

    def test_missing_components_are_reported_not_hidden(self):
        result = scoring.score({"audience_fit": {"smb_concentration": 5}})
        self.assertEqual(len(result["score_breakdown"]["audience_fit"]["missing"]), 4)
        self.assertLess(result["coverage"], 0.2)

    def test_out_of_range_is_rejected(self):
        with self.assertRaises(scoring.ScoringError):
            scoring.score({"audience_fit": {"smb_concentration": 9}})

    def test_unknown_component_is_rejected(self):
        with self.assertRaises(scoring.ScoringError):
            scoring.score({"audience_fit": {"vibes": 5}})

    def test_weights_sum_to_one_hundred(self):
        self.assertEqual(sum(s["max"] for s in scoring.DIMENSIONS.values()), 100)

    def test_partner_tier(self):
        self.assertEqual(scoring.partner_tier("STRATEGIC", "local"), "A")
        self.assertEqual(scoring.partner_tier("TIER_1", "national"), "A")
        self.assertEqual(scoring.partner_tier("TIER_1", "local"), "B")
        self.assertEqual(scoring.partner_tier("TIER_2", "local"), "C")
        self.assertEqual(scoring.partner_tier("NURTURE", "local"), "D")


if __name__ == "__main__":
    unittest.main()
