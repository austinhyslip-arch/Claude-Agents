"""Attio sync planning refuses to leak a non-public contact into the CRM."""

import copy
import unittest

import helpers
from eco import attio


class AttioPlanTest(unittest.TestCase):
    def setUp(self):
        self.org = copy.deepcopy(helpers.ORG)
        self.contact = copy.deepcopy(helpers.CONTACT)

    def test_company_values_use_real_attio_fields_only(self):
        values = attio.company_values(self.org)
        self.assertTrue(set(values).issubset(attio.COMPANY_FIELDS), set(values))

    def test_person_values_use_real_attio_fields_only(self):
        values = attio.person_values(self.contact, self.org["domain"])
        self.assertTrue(set(values).issubset(attio.PERSON_FIELDS), set(values))

    def test_person_without_public_email_is_refused(self):
        c = dict(self.contact, email_status="not_publicly_found", email=None)
        with self.assertRaises(ValueError):
            attio.person_values(c)

    def test_plan_skips_a_non_public_contact_and_says_why(self):
        c = dict(self.contact, email_status="not_publicly_found", email=None)
        plan = attio.plan(self.org, [c])
        skipped = [call for call in plan["calls"] if call.get("skipped")]
        self.assertEqual(len(skipped), 1)
        self.assertIn("no enrichment", skipped[0]["why"].lower())

    def test_plan_always_requires_human_approval(self):
        self.assertTrue(attio.plan(self.org, [self.contact])["requires_human_approval"])

    def test_missing_attributes_are_listed_not_silently_dropped(self):
        plan = attio.plan(self.org, [self.contact])
        names = [a[0] for a in plan["missing_attributes"]["companies"]]
        self.assertIn("ecosystem_state", names)
        self.assertIn("organization_score", names)

    def test_note_marks_an_estimate_as_an_estimate(self):
        org = dict(self.org, audience_confidence="ESTIMATE")
        body = attio.note_body(org)
        self.assertIn("ESTIMATE", body)

    def test_note_records_that_no_enrichment_was_used(self):
        self.assertIn("No enrichment provider was used",
                      attio.note_body(self.org, [self.contact]))

    def test_description_flags_estimated_audience(self):
        org = dict(self.org, audience_confidence="ESTIMATE")
        self.assertIn("Estimated audience (not stated by the organization)",
                      attio._describe(org))


if __name__ == "__main__":
    unittest.main()
