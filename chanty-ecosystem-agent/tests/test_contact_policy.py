"""The contact data rules. These are the tests that matter most."""

import copy
import unittest

import helpers
from eco import gates, policy


class GuessedEmailTest(unittest.TestCase):
    def test_email_without_a_source_url_fails(self):
        c = copy.deepcopy(helpers.CONTACT)
        c["email_source_url"] = None
        result = gates.check_contact_data_policy(c)
        self.assertFalse(result.passed)
        self.assertIn("email_has_source_url", [f["check"] for f in result.failures])

    def test_email_from_a_non_public_method_fails(self):
        c = copy.deepcopy(helpers.CONTACT)
        c["email_discovery_method"] = None
        c["email_source_url"] = "https://app.apollo.io/contact/123"
        result = gates.check_contact_data_policy(c)
        self.assertFalse(result.passed)
        self.assertIn("email_source_permitted", [f["check"] for f in result.failures])

    def test_pattern_guessed_email_fails_on_markers(self):
        c = copy.deepcopy(helpers.CONTACT)
        c["email"] = "jordan.rivera@example-valley-chamber.test"
        c["email_discovery_method"] = "staff_page"
        c["email_source_url"] = "https://example-valley-chamber.test/staff#pattern-inferred"
        result = gates.check_contact_data_policy(c)
        self.assertFalse(result.passed)
        self.assertIn("no_guess_markers", [f["check"] for f in result.failures])

    def test_D_level_source_is_not_good_enough_for_an_email(self):
        c = copy.deepcopy(helpers.CONTACT)
        c["email_source_type"] = "D"
        result = gates.check_contact_data_policy(c)
        self.assertFalse(result.passed)
        self.assertIn("email_source_type_not_D", [f["check"] for f in result.failures])

    def test_not_publicly_found_must_not_carry_an_address(self):
        c = copy.deepcopy(helpers.CONTACT)
        c["email_status"] = "not_publicly_found"
        result = gates.check_contact_data_policy(c)
        self.assertFalse(result.passed)
        self.assertIn("no_email_without_public_status", [f["check"] for f in result.failures])

    def test_not_publicly_found_passes_when_escalated_and_empty(self):
        c = copy.deepcopy(helpers.CONTACT)
        c.update({"email_status": "not_publicly_found", "email": None,
                  "requires_user_permission": True})
        self.assertTrue(gates.check_contact_data_policy(c).passed)


class EnrichmentTest(unittest.TestCase):
    def test_enrichment_without_authorization_fails(self):
        c = copy.deepcopy(helpers.CONTACT)
        c["enrichment_used"] = True
        c["enrichment_authorized_by"] = None
        result = gates.check_contact_data_policy(c)
        self.assertFalse(result.passed)
        self.assertIn("no_unauthorized_enrichment", [f["check"] for f in result.failures])

    def test_apollo_tools_are_blocked(self):
        for tool in ("mcp__Apollo_io__apollo_people_match",
                     "mcp__Apollo_io__apollo_contacts_search",
                     "mcp__ZoomInfo__enrich_contacts",
                     "mcp__ZoomInfo__search_contacts"):
            self.assertFalse(gates.check_tool_permitted(tool).passed, tool)

    def test_clay_contact_enrichment_is_blocked_but_company_tools_are_not(self):
        self.assertFalse(gates.check_tool_permitted(
            "mcp__Clay__find-and-enrich-contacts-at-company").passed)
        self.assertFalse(gates.check_tool_permitted(
            "mcp__Clay__find-and-enrich-list-of-contacts").passed)
        self.assertTrue(gates.check_tool_permitted(
            "mcp__Clay__find-and-enrich-company").passed)

    def test_public_research_tools_are_allowed(self):
        for tool in ("WebSearch", "WebFetch", "mcp__Attio__search-records"):
            self.assertTrue(gates.check_tool_permitted(tool).passed, tool)

    def test_policy_ships_with_enrichment_off(self):
        self.assertFalse(policy.enrichment_allowed())


if __name__ == "__main__":
    unittest.main()
