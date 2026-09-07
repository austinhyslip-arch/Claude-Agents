# Chanty prospecting pipeline - working state

Last run: 2026-09-07

## Done

**19 confirmed-email contacts pushed to Attio.** Companies, people and Pipeline
list entries all created. The handoff listed these as "ready to push" but they
had never actually landed in Attio - checked by search before writing, and none
of them were there.

**600 companies contact-searched across all three bands.** Every call so far has
been a free ZoomInfo search. Yield is 279 contacts in
`pending-enrichment.tsv`, each with a ZoomInfo personId so they can be enriched
later without paying to re-find them.

| Band | Companies in band | Searched | Contacts | Has email on file |
|------|------------------|----------|----------|-------------------|
| Sub-20 | ~539 | 400 | 181 | 120 (66%) |
| 20-99 | ~353 | 100 | 41 | 30 (73%) |
| 100-499 | ~323 | 100 | 57 | 56 (98%) |

Band totals drift between calls because ZoomInfo intent data shifts through the
day. Re-pull rather than trusting these numbers exactly.

## Blocked

Clay's Work Email waterfall returns "Credits are exhausted for this workspace",
so the cheap path is closed until the workspace is topped up.

## The email-coverage finding

`hasEmail` from the free search tells us, before spending anything, whether
ZoomInfo actually holds a business email for a contact. 206 of 279 do. Enriching
the other 73 would burn a bulk credit each and return nothing, so they are split
out into `no-email-on-file.tsv` and excluded from the enrich queue.

Coverage climbs sharply with company size: 66% at sub-20, 73% at 20-99, 98% at
100-499. Credits spent on the larger bands go much further.

## Not started

- Sub-20 pages 5-6, 20-99 pages 2-4, 100-499 pages 2-4 (~615 companies)
- Any enrichment
- Email sequence draft

## Notes for the next run

- Company 1334374792 (Allianz Commercial) is a large company miscategorised into
  the sub-20 band and floods contact searches with dozens of "product owner"
  titles. Excluded, as are Yale School of Management, LP Building Solutions,
  Aquinas College, MapQuest and Kay Jewelers for the same reason.
- Capped at 2 contacts per company. Some small businesses return 5-6 "owners"
  (Willow Creek III, Personal Travel, Shear Magic, HireQuest) and emailing all of
  them would read as spam.
- Titles containing "Product Owner", "Process Owner", "General Sales Manager" or
  "Marketing Operations" are not buyer titles for this pitch and were dropped.
- Travis Brown's email `travis@xtremelectrickc.com` sits on a domain one character
  off the company's actual `xtreme-electrickc.com`. Pushed to Attio as given but
  worth checking before anything is sent to him.
- `search_contacts` needs the deprecated `jobTitle` string with OR syntax. The
  `jobTitleList` array silently returns zero rows against multiple company IDs.
- `companyIdList` caps at 50 per call.
- When a search result is too large for the context, it gets written to a file
  instead. Parsing that file with python is far cheaper than reading it back.

## Files

- `pending-enrichment.tsv` - all 279 contacts, with personId and hasEmail
- `enrich-queue-has-email.tsv` - the 206 worth spending a credit on
- `no-email-on-file.tsv` - the 73 ZoomInfo has no business email for
- `companies-searched.txt` - the 499 company IDs already searched, so a resumed
  run skips them
