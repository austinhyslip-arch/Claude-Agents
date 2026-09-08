"""Outreach lands inside the recipient's working day, in their local time."""

import copy
import datetime
import unittest

import helpers
from eco import gates, timezones


def utc(y, m, d, h, mi=0):
    return datetime.datetime(y, m, d, h, mi, tzinfo=datetime.timezone.utc)


class TimezoneResolutionTest(unittest.TestCase):
    def test_unambiguous_state_is_a_known_fact(self):
        self.assertEqual(timezones.resolve("Asheville", "NC"),
                         ("America/New_York", "KNOWN_FACT"))

    def test_split_state_city_override_is_a_known_fact(self):
        self.assertEqual(timezones.resolve("Chattanooga", "TN"),
                         ("America/New_York", "KNOWN_FACT"))
        self.assertEqual(timezones.resolve("Nashville", "TN"),
                         ("America/Chicago", "KNOWN_FACT"))

    def test_split_state_unknown_city_is_only_an_estimate(self):
        name, conf = timezones.resolve("Smallville", "TN")
        self.assertEqual(name, "America/Chicago")
        self.assertEqual(conf, "ESTIMATE")

    def test_unknown_state_resolves_to_nothing(self):
        self.assertEqual(timezones.resolve("Somewhere", "ZZ"), (None, "UNKNOWN"))

    def test_non_us_is_not_guessed(self):
        self.assertEqual(timezones.resolve("Toronto", "ON", "CA"), (None, "UNKNOWN"))


class SendWindowTest(unittest.TestCase):
    def setUp(self):
        # Eastern chamber, so local time is UTC-4 in September.
        self.org = dict(copy.deepcopy(helpers.ORG), city="Asheville", state_region="NC",
                        country="US", timezone="America/New_York",
                        timezone_confidence="KNOWN_FACT")

    def _ok(self, when):
        return gates.check_send_window(self.org, now=when).passed

    def test_inside_the_working_day_passes(self):
        self.assertTrue(self._ok(utc(2026, 9, 8, 14)))   # 10:00 EDT, Tuesday

    def test_before_eight_local_is_blocked(self):
        self.assertFalse(self._ok(utc(2026, 9, 8, 11)))  # 07:00 EDT

    def test_after_five_local_is_blocked(self):
        self.assertFalse(self._ok(utc(2026, 9, 8, 22)))  # 18:00 EDT

    def test_exactly_eight_is_allowed_and_exactly_five_is_not(self):
        self.assertTrue(self._ok(utc(2026, 9, 8, 12)))    # 08:00 EDT
        self.assertFalse(self._ok(utc(2026, 9, 8, 21)))   # 17:00 EDT

    def test_weekends_are_blocked(self):
        result = gates.check_send_window(self.org, now=utc(2026, 9, 12, 14))  # Saturday
        self.assertFalse(result.passed)
        self.assertIn("is_a_weekday", [f["check"] for f in result.failures])

    def test_the_window_follows_the_recipient_not_us(self):
        """The same instant is fine for one chamber and too early for another."""
        pacific = dict(self.org, city="Salem", state_region="OR",
                       timezone="America/Los_Angeles")
        when = utc(2026, 9, 8, 13)  # 09:00 Eastern, 06:00 Pacific
        self.assertTrue(gates.check_send_window(self.org, now=when).passed)
        self.assertFalse(gates.check_send_window(pacific, now=when).passed)

    def test_an_estimated_timezone_narrows_the_window(self):
        est = dict(self.org, timezone_confidence="ESTIMATE")
        window = gates.send_window(est)
        self.assertEqual((window["start_hour"], window["end_hour"]), (9, 16))
        self.assertFalse(gates.check_send_window(est, now=utc(2026, 9, 8, 12)).passed)
        self.assertTrue(gates.check_send_window(est, now=utc(2026, 9, 8, 14)).passed)

    def test_an_unknown_timezone_blocks_rather_than_guessing(self):
        unknown = dict(self.org, timezone=None, timezone_confidence="UNKNOWN",
                       city="Somewhere", state_region="ZZ", country="US")
        result = gates.check_send_window(unknown, now=utc(2026, 9, 8, 14))
        self.assertFalse(result.passed)
        self.assertIn("timezone_known", [f["check"] for f in result.failures])

    def test_next_send_time_skips_to_the_morning(self):
        nxt = gates.next_send_time(self.org, now=utc(2026, 9, 8, 3))  # 23:00 Mon EDT
        self.assertEqual((nxt.weekday(), nxt.hour), (1, 8))           # Tue 08:00

    def test_next_send_time_skips_the_weekend(self):
        nxt = gates.next_send_time(self.org, now=utc(2026, 9, 12, 14))  # Saturday
        self.assertEqual((nxt.weekday(), nxt.hour), (0, 8))             # Monday 08:00

    def test_next_send_time_is_now_when_the_window_is_open(self):
        when = utc(2026, 9, 8, 14)
        self.assertEqual(gates.next_send_time(self.org, now=when).hour, 10)


class SendGateIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.root = helpers.temp_root()
        helpers.silence_audit(self)
        from eco import store
        self.org = dict(copy.deepcopy(helpers.ORG), city="Asheville", state_region="NC",
                        timezone="America/New_York", timezone_confidence="KNOWN_FACT")
        self.contact = copy.deepcopy(helpers.CONTACT)
        self.opp = copy.deepcopy(helpers.OPPORTUNITY)
        for coll, rec in (("organizations", self.org), ("contacts", self.contact),
                          ("opportunities", self.opp)):
            store.put(coll, rec, root=self.root, log=False)

    def _send(self, when):
        return gates.check_send(self.org, self.contact, helpers.DRAFT, self.opp,
                                root=self.root, human_approved=True, now=when)

    def test_send_gate_passes_inside_the_window(self):
        result = self._send(utc(2026, 9, 8, 14))
        self.assertTrue(result.passed, [f["check"] for f in result.failures])

    def test_send_gate_blocks_at_three_in_the_morning(self):
        result = self._send(utc(2026, 9, 8, 7))  # 03:00 EDT
        self.assertFalse(result.passed)
        self.assertIn("send_window", [f["check"] for f in result.failures])

    def test_human_approval_does_not_override_the_window(self):
        """Approving a message does not make 3am an acceptable time to receive it."""
        self.assertFalse(self._send(utc(2026, 9, 8, 7)).passed)


if __name__ == "__main__":
    unittest.main()
