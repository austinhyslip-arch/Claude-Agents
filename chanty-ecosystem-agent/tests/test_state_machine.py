"""State transitions are explicit or they do not happen."""

import copy
import unittest

import helpers
from eco import state_machine as sm


class TransitionTest(unittest.TestCase):
    def setUp(self):
        helpers.silence_audit(self)
        self.org = copy.deepcopy(helpers.ORG)
        self.org["state"] = "DISCOVERED"

    def test_legal_path_works(self):
        sm.apply(self.org, "start_research")
        self.assertEqual(self.org["state"], "RESEARCHING")
        sm.apply(self.org, "qualify")
        sm.apply(self.org, "identify_contact")
        sm.apply(self.org, "ready_for_outreach",
                 context={"qualification_gates_passed": True})
        self.assertEqual(self.org["state"], "READY_FOR_OUTREACH")

    def test_skipping_research_is_rejected(self):
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "qualify")

    def test_unknown_event_is_rejected(self):
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "just_send_it")

    def test_ready_for_outreach_requires_the_gate_result(self):
        self.org["state"] = "CONTACT_IDENTIFIED"
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "ready_for_outreach", context={"qualification_gates_passed": False})

    def test_start_outreach_requires_send_authorization(self):
        self.org["state"] = "READY_FOR_OUTREACH"
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "start_outreach")
        sm.apply(self.org, "start_outreach", context={"send_authorized": True})
        self.assertEqual(self.org["state"], "OUTREACH_ACTIVE")

    def test_partner_won_is_human_only(self):
        self.org["state"] = "PARTNERSHIP_NEGOTIATION"
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "partner_won", actor="agent")
        sm.apply(self.org, "partner_won", actor="human")
        self.assertEqual(self.org["state"], "PARTNER_WON")

    def test_suppressed_is_terminal_for_agents(self):
        sm.apply(self.org, "suppress")
        self.assertEqual(self.org["state"], "SUPPRESSED")
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "start_research")
        sm.apply(self.org, "human_override", actor="human", target_state="NURTURE")
        self.assertEqual(self.org["state"], "NURTURE")

    def test_override_needs_a_real_target(self):
        with self.assertRaises(sm.TransitionError):
            sm.apply(self.org, "human_override", actor="human", target_state="SENT_ALREADY")

    def test_history_records_every_move(self):
        sm.apply(self.org, "start_research")
        sm.apply(self.org, "qualify")
        self.assertEqual([h["to"] for h in self.org["state_history"]],
                         ["RESEARCHING", "QUALIFIED"])
        self.assertTrue(all(h["actor"] for h in self.org["state_history"]))


class AutonomyTest(unittest.TestCase):
    def test_level_zero_never_permits_sending(self):
        permitted, why = sm.outreach_permitted(dict(helpers.ORG, partner_tier="C",
                                                    priority_band="TIER_2"))
        self.assertFalse(permitted)
        self.assertIn("draft-only", why)

    def test_tier_a_is_never_automatic(self):
        permitted, why = sm.outreach_permitted(dict(helpers.ORG, partner_tier="A"))
        self.assertFalse(permitted)
        self.assertIn("human-approved", why)


if __name__ == "__main__":
    unittest.main()
