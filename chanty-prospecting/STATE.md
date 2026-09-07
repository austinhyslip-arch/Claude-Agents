# Chanty prospecting pipeline - working state

Last run: 2026-09-07

## Done

**105 contacts are now in Attio** as People, linked to Companies, and added to
the Pipeline list with an `industry` value on each entry.

- 19 from the earlier handoff. Those had been listed as "ready to push" but had
  never actually landed in Attio, checked by search before writing.
- 86 enriched in this run, covering the 20-99 and 100-499 bands.

**86 ZoomInfo enrichments, 86 successes, no errors.** Every contact in the queue
was flagged `hasEmail=Y` by the free search first, and every one came back with
a real business email. That flag is reliable.

**600 companies contact-searched across all three bands.** All free searches.
Yield is 279 contacts in `pending-enrichment.tsv`, each with a ZoomInfo personId
so they can be enriched later without paying to re-find them.

| Band | Companies in band | Searched | Contacts | Has email on file | Enriched |
|------|------------------|----------|----------|-------------------|----------|
| Sub-20 | ~539 | 400 | 181 | 120 (66%) | 0 |
| 20-99 | ~353 | 100 | 41 | 30 (73%) | 30 |
| 100-499 | ~323 | 100 | 57 | 56 (98%) | 56 |

Band totals drift between calls because ZoomInfo intent data shifts through the
day. Re-pull rather than trusting these numbers exactly.

## Blocked

Clay's Work Email waterfall returns "Credits are exhausted for this workspace",
so the cheap path is closed until the workspace is topped up. Everything since
has gone through paid ZoomInfo enrichment instead.

## The email-coverage finding

`hasEmail` from the free search tells us, before spending anything, whether
ZoomInfo actually holds a business email for a contact. 206 of 279 do. Enriching
the other 73 would burn a bulk credit each and return nothing, so they are split
out into `no-email-on-file.tsv` and excluded from the enrich queue. That saved
73 credits, about a quarter of the list.

Coverage climbs sharply with company size: 66% at sub-20, 73% at 20-99, 98% at
100-499. Credits spent on the larger bands go much further, which is why those
two bands were enriched first.

## Open decisions

- Whether to enrich the remaining 120 sub-20 contacts flagged `hasEmail=Y`.
  That is 120 bulk credits for the weakest-coverage band.
- Whether to act on `pattern-derivable.tsv`, the 18 contacts whose company email
  format we already know for free. Worth doing, but verify before sending. Six
  companies in this set use an email domain different from their website domain
  (tas.com, tc-mro.com, hirequestllc.com, mobileonsite.com, dsarms.com,
  turbine-controls.com), so a guessed address can bounce.

## Not started

- Sub-20 pages 5-6, 20-99 pages 2-4, 100-499 pages 2-4 (~615 companies)
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
- Attio has no bulk import. Each contact takes three calls: upsert the company on
  `domains`, upsert the person on `email_addresses` with `company` set to the
  website domain, then `add-record-to-list`.
- Attio auto-enriches companies after creation and fills in `categories`. The
  `industry` values on the Pipeline entries were derived from those categories,
  which is free. It also auto-creates a second company record off the email
  domain when that differs from the website domain, so a domain like tas.com can
  show up twice. Match on the record id from the person's `company` link, not on
  the domain string.

## Files

- `pending-enrichment.tsv` - all 279 contacts, with personId and hasEmail
- `enrich-queue-has-email.tsv` - the 206 worth spending a credit on
- `no-email-on-file.tsv` - the 73 ZoomInfo has no business email for
- `enrich-now.tsv` - the 86 that were enriched in this run
- `enriched.tsv` - the 86 enrichment results, with emails
- `attio-push.tsv` - `enriched.tsv` joined to each company's website domain
- `attio-records.tsv` - the Attio person and company record ids, plus the
  industry written to each Pipeline entry
- `pattern-derivable.tsv` - 18 contacts whose company email format we already know
- `no-pattern-available.tsv` - the other 55 dark contacts
- `public-sources-test.md` - what the public-source search actually returned
- `companies-searched.txt` - the 499 company IDs already searched, so a resumed
  run skips them
