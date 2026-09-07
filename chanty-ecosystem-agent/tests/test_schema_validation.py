"""Records validate before they are written, and bad records do not get written."""

import copy
import json
import os
import unittest

import helpers
from eco import paths, store, validate


class ValidatorTest(unittest.TestCase):
    def test_all_schemas_parse(self):
        for name in paths.COLLECTIONS.values():
            with open(os.path.join(paths.SCHEMA_DIR, name)) as fh:
                json.load(fh)

    def test_good_records_validate(self):
        validate.validate(helpers.ORG, store.schema("organizations"))
        validate.validate(helpers.CONTACT, store.schema("contacts"))
        validate.validate(helpers.OPPORTUNITY, store.schema("opportunities"))

    def test_missing_required_field_fails(self):
        bad = copy.deepcopy(helpers.ORG)
        del bad["organization_name"]
        with self.assertRaises(validate.ValidationError):
            validate.validate(bad, store.schema("organizations"))

    def test_unexpected_field_fails(self):
        bad = dict(helpers.ORG, secret_score=99)
        with self.assertRaises(validate.ValidationError):
            validate.validate(bad, store.schema("organizations"))

    def test_bad_enum_fails(self):
        bad = dict(helpers.CONTACT, email_status="probably_right")
        with self.assertRaises(validate.ValidationError):
            validate.validate(bad, store.schema("contacts"))

    def test_bad_id_pattern_fails(self):
        bad = dict(helpers.ORG, organization_id="chamber-1")
        with self.assertRaises(validate.ValidationError):
            validate.validate(bad, store.schema("organizations"))

    def test_score_out_of_range_fails(self):
        bad = dict(helpers.ORG, organization_score=120)
        with self.assertRaises(validate.ValidationError):
            validate.validate(bad, store.schema("organizations"))

    def test_nested_evidence_is_validated(self):
        bad = copy.deepcopy(helpers.ORG)
        bad["evidence"][0]["source_type"] = "Z"
        with self.assertRaises(validate.ValidationError):
            validate.validate(bad, store.schema("organizations"))

    def test_invalid_record_is_not_written(self):
        root = helpers.temp_root()
        helpers.silence_audit(self)
        bad = dict(helpers.ORG, organization_score=500)
        with self.assertRaises(validate.ValidationError):
            store.put("organizations", bad, root=root, log=False)
        self.assertEqual(store.all("organizations", root=root), [])

    def test_null_is_accepted_where_the_schema_allows_it(self):
        ok = dict(helpers.ORG, linkedin=None, parent_organization=None)
        validate.validate(ok, store.schema("organizations"))


if __name__ == "__main__":
    unittest.main()
