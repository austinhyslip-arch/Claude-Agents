"""Deduplication, including the chapter rule."""

import copy
import unittest

import helpers
from eco import dedupe, store


class DedupeTest(unittest.TestCase):
    def setUp(self):
        self.root = helpers.temp_root()
        helpers.silence_audit(self)
        store.put("organizations", copy.deepcopy(helpers.ORG), root=self.root, log=False)
        self.existing = store.all("organizations", root=self.root)

    def _dupe(self, candidate):
        return dedupe.find_duplicate(candidate, existing=self.existing)

    def test_same_domain_is_a_duplicate(self):
        rec, reason = self._dupe({"organization_name": "Example Valley Chamber",
                                  "website": "http://www.example-valley-chamber.test/about"})
        self.assertIsNotNone(rec)
        self.assertEqual(reason, "exact_domain")

    def test_name_variants_are_a_duplicate(self):
        rec, reason = self._dupe({"organization_name": "The Example Valley Chamber of Commerce, Inc."})
        self.assertIsNotNone(rec)
        self.assertEqual(reason, "normalized_name")

    def test_linkedin_url_is_a_duplicate(self):
        self.existing[0]["linkedin"] = "https://www.linkedin.com/company/example-valley-chamber/"
        rec, reason = self._dupe({"organization_name": "Totally Different Name",
                                  "linkedin": "linkedin.com/company/example-valley-chamber"})
        self.assertEqual(reason, "linkedin_url")

    def test_a_different_organization_is_not_a_duplicate(self):
        rec, _ = self._dupe({"organization_name": "Northside Business Alliance",
                             "website": "https://northside-alliance.test"})
        self.assertIsNone(rec)

    def test_chapters_of_the_same_parent_are_not_merged(self):
        national = {"organization_name": "National Widget Association",
                    "website": "https://widgets.test", "chapter": None}
        kansas = {"organization_name": "National Widget Association",
                  "website": "https://widgets.test", "chapter": "Kansas"}
        missouri = {"organization_name": "National Widget Association",
                    "website": "https://widgets.test", "chapter": "Missouri"}
        pool = []
        for candidate in (national, kansas, missouri):
            rec, _ = dedupe.find_duplicate(candidate, existing=pool)
            self.assertIsNone(rec, candidate.get("chapter"))
            pool.append(dict(candidate, organization_id=dedupe.proposed_id(candidate)))
        self.assertEqual(len({p["organization_id"] for p in pool}), 3)

    def test_the_same_chapter_twice_is_a_duplicate(self):
        kansas = {"organization_name": "National Widget Association",
                  "website": "https://widgets.test", "chapter": "Kansas"}
        pool = [dict(kansas, organization_id=dedupe.proposed_id(kansas))]
        rec, reason = dedupe.find_duplicate(dict(kansas), existing=pool)
        self.assertIsNotNone(rec)

    def test_ids_are_stable_across_runs(self):
        a = dedupe.proposed_id({"organization_name": "X", "website": "https://x.test"})
        b = dedupe.proposed_id({"organization_name": "X", "website": "http://www.x.test/"})
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
