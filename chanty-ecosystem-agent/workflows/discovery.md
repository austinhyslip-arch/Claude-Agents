# Workflow: Discovery

Input: a category and a count, e.g. chambers 100.
Output: verified, deduplicated organization records in DISCOVERED.
Contacts nobody.

1. Read `agents/discovery.md`.
2. Break the target into slices: one category, one geography, one search pass.
   Chambers in Kansas City, then chambers in Wichita. Not "chambers".
3. For each candidate:
   a. Open the organization's own site. No site, no record.
   b. Pull audience, distribution mechanisms, geography, parent and chapter.
   c. Capture at least two pieces of A or B evidence with URLs and dates.
   d. `python3 -m eco dedupe-check '<json>'`
   e. If not a duplicate, `python3 -m eco add-org '<json>'`
4. Report: found, verified, duplicates skipped, created, and the categories that
   came up empty.

Stop conditions:
- A source that cannot be verified is dropped, not softened into a record.
- If the category yields fewer than half the target, report that rather than
  padding with weak records.
