# Chanty prospecting pipeline - working state

Last run: 2026-09-08

## Done

**105 contacts are in Attio** as People, linked to Companies, and added to the
Pipeline list with an `industry` value on each entry.

- 19 from the earlier handoff. Those had been listed as "ready to push" but had
  never actually landed in Attio, checked by search before writing.
- 86 enriched in the first run, covering the 20-99 and 100-499 bands.

**86 ZoomInfo enrichments, 86 successes, no errors.** Every contact in the queue
was flagged `hasEmail=Y` by the free search first, and every one came back with
a real business email. That flag is reliable.

**All three bands are now fully paginated.** 1,150 companies contact-searched,
all on free searches. Yield is 760 contacts in `all-contacts.tsv`, each with a
ZoomInfo personId so they can be enriched later without paying to re-find them.

| Band | Companies searched | Contacts | Has email on file | Enriched |
|------|-------------------|----------|-------------------|----------|
| Sub-20 | 580 | 268 | 175 (65%) | 0 |
| 20-99 | 353 | 202 | 158 (78%) | 30 |
| 100-499 | 323 | 290 | 257 (89%) | 56 |

The second run added 481 contacts on top of the original 279. Nothing
duplicated: checked by personId and by name plus company, both came back clean.

Per instruction, none of the sub-20 band was enriched in this run.

## Blocked

Clay's Work Email waterfall returns "Credits are exhausted for this workspace",
so the cheap path is closed until the workspace is topped up. Everything since
has gone through paid ZoomInfo enrichment instead.

## The email-coverage finding

`hasEmail` from the free search tells us, before spending anything, whether
ZoomInfo actually holds a business email for a contact. Across all 760 contacts,
590 do. Enriching the other 170 would burn a bulk credit each and return
nothing, so they are excluded from the enrich queue. That saves 170 credits,
about 22% of the list.

Coverage climbs with company size: 65% at sub-20, 78% at 20-99, 89% at 100-499.
Credits spent on the larger bands go further, which is why those two bands were
enriched first.

## Open decisions

- **504 contacts are flagged `hasEmail=Y` and not yet enriched**, listed in
  `remaining-has-email.tsv`: 201 at 100-499, 128 at 20-99, 175 at sub-20. Each
  costs one ZoomInfo bulk credit. The 100-499 and 20-99 sets are the better
  value; sub-20 was explicitly held back this run.
- Whether to act on `pattern-derivable.tsv`, the 18 contacts whose company email
  format we already know for free. Worth doing, but verify before sending. Six
  companies in that set use an email domain different from their website domain
  (tas.com, tc-mro.com, hirequestllc.com, mobileonsite.com, dsarms.com,
  turbine-controls.com), so a guessed address can bounce.

## Not started

- The email sequence draft.

## Notes for the next run

- Some companies are miscategorised into a small band and flood the contact
  search. Excluded so far: Allianz Commercial (1334374792), Yale School of
  Management, LP Building Solutions, Aquinas College, MapQuest, Kay Jewelers,
  New Country Lexus (460884745, ~50 general managers), Spokane Public Schools
  Foundation (55543959, 22 office managers across many schools, capped at 2
  rather than dropped) and 5LINX (197050531). 5LINX is the worst of them: it is
  a multi-level marketing company whose records are hundreds of "independent
  business owners", none of whom buy software for a team. Dropped entirely.
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

- `all-contacts.tsv` - all 760 contacts across both runs, with personId and hasEmail
- `round2-contacts.tsv` - just the 481 found in the second run
- `remaining-has-email.tsv` - the 504 flagged hasEmail=Y and not yet enriched
- `pending-enrichment.tsv` - the original 279 from the first run
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
- `companies-searched.txt` - the 1,150 company IDs already searched, so a
  resumed run skips them
