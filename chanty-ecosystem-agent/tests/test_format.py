"""Plain text, no sign-off. Gmail supplies both of the things we leave out."""

import unittest

import helpers  # noqa: F401
from eco import gates, gmail


CLEAN = ("Hi Jordan,\n\nI saw the chamber runs a monthly luncheon and the October "
         "slot is open.\n\nWe put together practical sessions on team communication "
         "for growing businesses. Happy to run one, no product pitch.\n\n"
         "We would join remotely rather than be in the room.\n\n"
         "Would that be useful?")


class FormatGateTest(unittest.TestCase):
    def test_a_clean_plain_text_draft_passes(self):
        self.assertTrue(gates.check_format(CLEAN).passed)

    def test_thanks_mid_body_is_not_a_sign_off(self):
        body = ("Hi Jordan,\n\nThanks for putting the events page together, it made "
                "this easy to find.\n\nWould a session be useful for October?")
        self.assertTrue(gates.check_format(body).passed)

    def test_a_hyphen_mid_sentence_is_not_a_bullet(self):
        body = ("Hi Jordan,\n\nMost of your members are 10-50 people, which is the "
                "size where this gets messy.\n\nWould that be useful?")
        self.assertTrue(gates.check_format(body).passed)

    def test_sign_offs_are_blocked(self):
        for tail in ("\n\nBest,\nAustin", "\n\nThanks", "\n\nCheers,", "\n\nRegards,\nAustin",
                     "\n\nSincerely,", "\n\nTalk soon", "\n\nAll the best,\nAustin"):
            result = gates.check_format(CLEAN + tail)
            self.assertFalse(result.passed, tail)
            self.assertIn("no_sign_off", [f["check"] for f in result.failures])

    def test_formatting_is_blocked(self):
        for body in (CLEAN + "\n\n- one\n- two",
                     CLEAN + "\n\n1. one\n2. two",
                     CLEAN.replace("useful", "**useful**"),
                     CLEAN + "\n\n## Next steps",
                     CLEAN + "\n\nHere is the [outline](https://example.test).",
                     CLEAN + "\n\n> quoted line",
                     "Hi Jordan,<br>Would that be useful?",
                     CLEAN + "\n\n`code`",
                     CLEAN + "\n\n---"):
            result = gates.check_format(body)
            self.assertFalse(result.passed, body[-30:])
            self.assertIn("no_markdown_or_html", [f["check"] for f in result.failures])

    def test_unsubscribe_token_is_blocked(self):
        result = gates.check_format(CLEAN + "\n\n{{unsubscribe_url}}")
        self.assertIn("no_unsubscribe_token", [f["check"] for f in result.failures])

    def test_an_empty_body_is_blocked(self):
        self.assertFalse(gates.check_format("").passed)


class GmailPayloadTest(unittest.TestCase):
    def setUp(self):
        self.contact = dict(helpers.CONTACT)
        self.draft = dict(helpers.DRAFT, body=CLEAN)

    def test_payload_never_sets_html_body(self):
        args = gmail.build(self.draft, self.contact)
        self.assertNotIn("htmlBody", args)
        self.assertEqual(args["to"], [self.contact["email"]])
        self.assertTrue(args["subject"])

    def test_body_is_passed_through_as_plain_text(self):
        args = gmail.build(self.draft, self.contact)
        self.assertIn("Would that be useful?", args["body"])
        self.assertNotIn("<", args["body"])

    def test_a_sign_off_is_refused_before_a_payload_exists(self):
        draft = dict(self.draft, body=CLEAN + "\n\nBest,\nAustin")
        with self.assertRaises(gmail.DraftRejected):
            gmail.build(draft, self.contact)

    def test_a_non_public_contact_is_refused(self):
        contact = dict(self.contact, email_status="not_publicly_found", email=None)
        with self.assertRaises(gmail.DraftRejected) as ctx:
            gmail.build(self.draft, contact)
        self.assertIn("contact_email_public", str(ctx.exception))

    def test_a_prohibited_claim_is_refused(self):
        draft = dict(self.draft, body=CLEAN + "\n\nWe can offer your members a discount.")
        with self.assertRaises(gmail.DraftRejected):
            gmail.build(draft, self.contact)

    def test_an_empty_subject_is_refused(self):
        draft = dict(self.draft, subject="  ")
        with self.assertRaises(gmail.DraftRejected):
            gmail.build(draft, self.contact)

    def test_plan_carries_the_review_context(self):
        plan = gmail.plan(self.draft, self.contact, helpers.ORG)
        self.assertEqual(plan["tool"], "mcp__Gmail__create_draft")
        self.assertEqual(plan["sending_mode"], "manual_gmail_draft")
        self.assertEqual(plan["review_context"]["contact"], "Jordan Rivera")
        self.assertTrue(plan["review_context"]["evidence"])


if __name__ == "__main__":
    unittest.main()


class DeliveryDisclosureTest(unittest.TestCase):
    """Live session offers have to say we join remotely."""

    SESSION = "Hi Amy,\n\nWe would run a session on team communication.\n\nWould that fit?"

    def test_workshop_without_the_disclosure_is_blocked(self):
        result = gates.check_delivery_disclosure(self.SESSION, "educational_workshop")
        self.assertFalse(result.passed)
        self.assertIn("states_remote_delivery", [f["check"] for f in result.failures])

    def test_event_participation_without_the_disclosure_is_blocked(self):
        self.assertFalse(
            gates.check_delivery_disclosure(self.SESSION, "event_participation").passed)

    def test_any_of_the_accepted_phrasings_passes(self):
        for phrase in ("we would join remotely", "we would join by video",
                       "we would present over video", "we would join virtually",
                       "we are not in person for these", "we would not be in the room"):
            body = self.SESSION + "\n\n" + phrase.capitalize() + "."
            self.assertTrue(
                gates.check_delivery_disclosure(body, "educational_workshop").passed, phrase)

    def test_written_offers_need_no_disclosure(self):
        for offer in ("member_resource", "co_branded_content", "member_benefit",
                      "partner_referral_program", "discovery_conversation"):
            self.assertTrue(gates.check_delivery_disclosure(self.SESSION, offer).passed, offer)

    def test_gmail_refuses_a_workshop_draft_that_omits_it(self):
        without = CLEAN.replace(
            "We would join remotely rather than be in the room.\n\n", "")
        draft = dict(helpers.DRAFT, offer="educational_workshop", body=without)
        with self.assertRaises(gmail.DraftRejected) as ctx:
            gmail.build(draft, dict(helpers.CONTACT))
        self.assertIn("states_remote_delivery", str(ctx.exception))

    def test_gmail_accepts_it_once_the_line_is_there(self):
        draft = dict(helpers.DRAFT, offer="educational_workshop", body=CLEAN)
        self.assertIn("remotely", gmail.build(draft, dict(helpers.CONTACT))["body"])

    def test_the_constraint_is_configured_in_policy(self):
        from eco import policy
        dc = policy.get("delivery_constraints")
        self.assertTrue(dc["live_sessions_are_remote_only"])
        self.assertFalse(dc["travel_budget_exists"])
        self.assertEqual(sorted(dc["offers_requiring_disclosure"]),
                         ["educational_workshop", "event_participation"])
