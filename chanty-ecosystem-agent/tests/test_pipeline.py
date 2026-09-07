"""End to end, through the actual CLI, in a throwaway data directory.

This is the run described in the spec's example: discover, dedupe, research,
score, qualify, find a contact, detect a signal, draft, and then stop. The last
assertion is the important one: the pipeline ends at human review, not at a send.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

import helpers

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.data = tempfile.mkdtemp(prefix="eco-pipeline-")
        self.logs = tempfile.mkdtemp(prefix="eco-pipeline-logs-")
        self.env = dict(os.environ, ECO_DATA_DIR=self.data, ECO_LOG_DIR=self.logs,
                        PYTHONPATH=SCRIPTS)

    def eco(self, *args, expect=0):
        proc = subprocess.run([sys.executable, "-m", "eco", *args], env=self.env,
                              cwd=SCRIPTS, capture_output=True, text=True)
        self.assertEqual(proc.returncode, expect,
                         "eco %s\nstdout: %s\nstderr: %s" % (" ".join(args), proc.stdout, proc.stderr))
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            return proc.stdout

    def test_full_run_stops_before_sending(self):
        candidate = {k: v for k, v in helpers.ORG.items()
                     if k not in ("organization_id", "state", "state_history", "priority_band",
                                  "partner_tier", "trials", "paid_accounts", "seats", "mrr",
                                  "arr", "assisted_revenue", "created_at")}
        created = self.eco("add-org", json.dumps(candidate))
        self.assertTrue(created["created"])
        org_id = created["organization_id"]

        # The same organization discovered a second time is not created twice.
        again = self.eco("add-org", json.dumps(dict(candidate, website="http://www.example-valley-chamber.test/")))
        self.assertFalse(again["created"])
        self.assertEqual(again["duplicate_of"], org_id)

        self.eco("transition", org_id, "start_research")
        scored = self.eco("score", org_id, json.dumps({
            "audience_fit": {"smb_concentration": 5, "employee_size_fit": 4,
                             "team_communication_need": 4, "vertical_relevance": 3,
                             "geographic_reach": 2},
            "distribution_power": {"email_newsletter": 5, "webinars_workshops": 2,
                                   "events": 4, "member_client_communication": 4,
                                   "community_directory_repeat_exposure": 3},
            "partnership_compatibility": {"technology_sponsors": 3, "member_benefits": 4,
                                          "educational_partnerships": 4, "referral_structure": 2},
            "timing": {"upcoming_event": 4, "current_initiative": 2,
                       "leadership_or_program_change": 0},
            "strategic_value": {"multi_chapter_national_leverage": 1,
                                "potential_seat_volume": 3, "lookalike_potential": 3},
        }))
        self.assertGreater(scored["organization_score"], 50)
        self.eco("transition", org_id, "qualify")

        contact = dict(helpers.CONTACT, organization_id=org_id)
        contact.pop("contact_id")
        made = self.eco("add-contact", json.dumps(contact))
        self.assertTrue(made["created"])
        contact_id = made["contact_id"]
        self.eco("transition", org_id, "identify_contact")

        self.eco("add-signal", json.dumps({
            "organization_id": org_id, "signal_type": "event_announcement",
            "summary": "October member luncheon speaker slot listed as open",
            "signal_date": "2026-09-01T00:00:00+00:00",
            "source_url": "https://example-valley-chamber.test/events",
            "source_type": "A", "confidence": "KNOWN_FACT",
            "relevance": "the workshop offer maps directly to this slot",
        }))

        opportunity = dict(helpers.OPPORTUNITY, organization_id=org_id)
        opp_path = os.path.join(self.data, "opportunities", opportunity["opportunity_id"] + ".json")
        with open(opp_path, "w") as fh:
            json.dump(opportunity, fh)

        gate = self.eco("gate", org_id, "--contact-id", contact_id,
                        "--opportunity-id", opportunity["opportunity_id"])
        self.assertTrue(gate["passed"], gate["failures"])

        self.eco("transition", org_id, "ready_for_outreach")

        draft = dict(helpers.DRAFT, organization_id=org_id, contact_id=contact_id)
        self.assertTrue(self.eco("draft-check", json.dumps(draft))["passed"])

        # And here it stops: compliance is unconfigured and autonomy is level 0.
        blocked = self.eco("send-check", json.dumps(draft), expect=2)
        self.assertFalse(blocked["passed"])
        self.assertIn("email_compliance", blocked["failures"])
        self.assertIn("autonomy_or_human_approval", blocked["failures"])

        status = self.eco("status")
        self.assertEqual(status["outreach_sent"], 0)
        self.assertEqual(status["enrichment_used_count"], 0)
        self.assertEqual(status["autonomy_level"], 0)

        self.assertTrue(self.eco("validate")["valid"])

        with open(os.path.join(self.logs, "audit.jsonl")) as fh:
            audit_lines = fh.read().strip().split("\n")
        actions = [json.loads(line)["action"] for line in audit_lines]
        for expected in ("create_record", "state_transition", "score",
                         "qualification_gate", "send_gate", "dedupe_skip"):
            self.assertIn(expected, actions)

    def test_a_guessed_email_is_rejected_by_the_cli(self):
        candidate = {k: v for k, v in helpers.ORG.items()
                     if k not in ("organization_id", "state", "state_history", "priority_band",
                                  "partner_tier", "trials", "paid_accounts", "seats", "mrr",
                                  "arr", "assisted_revenue", "created_at")}
        org_id = self.eco("add-org", json.dumps(candidate))["organization_id"]
        guessed = dict(helpers.CONTACT, organization_id=org_id,
                       email="j.rivera@example-valley-chamber.test",
                       email_source_url=None, email_discovery_method=None)
        guessed.pop("contact_id")
        out = self.eco("add-contact", json.dumps(guessed), expect=2)
        self.assertFalse(out["created"])

    def test_blocked_tool_check_exits_nonzero(self):
        out = self.eco("check-tool", "mcp__Apollo_io__apollo_people_match", expect=3)
        self.assertFalse(out["passed"])

    def test_contact_report_prints_the_handoff_block(self):
        candidate = {k: v for k, v in helpers.ORG.items()
                     if k not in ("organization_id", "state", "state_history", "priority_band",
                                  "partner_tier", "trials", "paid_accounts", "seats", "mrr",
                                  "arr", "assisted_revenue", "created_at")}
        org_id = self.eco("add-org", json.dumps(candidate))["organization_id"]
        contact = dict(helpers.CONTACT, organization_id=org_id, email=None,
                       email_status="not_publicly_found", email_source_url=None,
                       email_source_type=None, email_date_checked=None,
                       email_discovery_method=None, requires_user_permission=True,
                       sources_checked=["https://example-valley-chamber.test/staff",
                                        "https://example-valley-chamber.test/contact"],
                       alternative_contact_methods=["general inbox listed on the contact page",
                                                    "public phone number"])
        contact.pop("contact_id")
        contact_id = self.eco("add-contact", json.dumps(contact))["contact_id"]
        text = self.eco("contact-report", contact_id)
        self.assertIn("Public email: NOT FOUND", text)
        self.assertIn("recommended_action = ASK_USER", text)
        self.assertIn("enrichment_used = false", text)

    def test_reports_run_on_an_empty_store(self):
        weekly = self.eco("report", "weekly")
        self.assertEqual(weekly["business"]["paid_seats"], 0)
        self.assertIn("paid seats", weekly["business"]["note"])
        self.eco("report", "monthly")
        self.eco("learn")


if __name__ == "__main__":
    unittest.main()
