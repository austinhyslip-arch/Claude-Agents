# Contact enrichment — free sources, then guessing, then paid tools

Order of operations for every contact, strictly in this sequence. Never skip ahead to a
paid tool because free sources are slow — skip ahead only when free sources are genuinely
exhausted for that specific field.

## 1. Free sources (always first)

- Company website — staff/about/team/contact pages. Small practices often list the office
  manager by name on the "About Us" or "Meet Our Team" page, sometimes with a direct email.
- Facebook business page — "About" tab, posts introducing staff, tagged photos with names.
- Press releases / local news — practice openings, community involvement pieces, award
  mentions often name the office manager or owner.
- NPI Registry — confirms the practice's authorized official name (often the owner) and
  taxonomy/specialty. Doesn't give office managers directly but is a reliable source for
  owner name and practice legitimacy.
- General web search — `"<practice name>" "office manager"` or `"<practice name>" "practice
  manager"` surfaces LinkedIn profiles, local news, and chamber-of-commerce bios.
- LinkedIn (via search, not scraping behind login) — a public profile showing current title
  and employer is a strong source for name + title; email is rarely public here.

Record `Email Source` = `Verified (free source)` only when the email itself (not just the
name/title) came from one of these — e.g. it was printed on a staff page or in a press
release, not inferred.

## 2. Email guessing (before any paid tool)

If a verified email isn't found through free sources but the person's name and the
company's domain are known, build a best guess.

**Domain**: from the company's own site (the domain already captured in the spreadsheet's
Domain column).

**Pattern-check first.** Before guessing blind, check whether any other email at this
domain is already known — from a press release byline, a staff page listing a different
employee's full email, a WHOIS/registrant contact, or a prior Attio record for the same
company. If one exists, its structure (first.last@, firstlast@, f.last@, first@, etc.) is
the pattern to reuse for this person's guess.

**Common structures to try, in order of general prevalence for small businesses:**
1. `first.last@domain`
2. `firstlast@domain`
3. `first@domain` (common at very small practices — under ~10 staff)
4. `flast@domain`
5. `first_last@domain`

**Confidence rating** — write it into `Email Guess Confidence` as a percentage plus the
reason, not just a number:
- `90% — pattern confirmed from another staff email at this domain`
- `65% — pattern inferred from company size and domain registrar conventions, no direct
  confirmation`
- `40% — no pattern reference, generic guess (first.last@ default)`

Set `Email Source` = `Guessed` and `Needs Paid Tool (Email)` = `No` for anything with a
guess in place — the guess is the deliverable at this stage, not a placeholder waiting on
Apollo.

## 3. When free sources and guessing aren't enough

Set `Email Source` = `Needs Paid Tool`, leave the guess fields blank or note why no guess
was possible (e.g. domain unknown), and set `Needs Paid Tool (Email)` = `Yes`. Do not call
Apollo or Hunter for this row.

## 4. Paid lookup (Apollo.io / Hunter.io) — only after Austin confirms

This only happens in a separate, later step: after Austin reviews the spreadsheet and tells
the agent which `Needs Paid Tool: Yes` rows to actually look up. At that point:
- Try Apollo's people-match/enrich first (already integrated, no per-lookup approval
  friction beyond the row-level confirmation already given).
- Use Hunter.io only for verifying an email Apollo can't produce or confirm, if Hunter
  access is available in the session.
- Update `Email Source` to `Verified (free source)` is wrong here — use a distinct note in
  the row (e.g. append " — paid lookup" isn't a defined column value; simplest is to update
  the email itself and set `Email Guess Confidence` to blank, `Needs Paid Tool (Email)` to
  `No` now that it's resolved) once the paid tool returns a result.

## Company-level enrichment (staff count, domain, location, LinkedIn)

Same ordering applies: company website, Facebook page, press releases, NPI Registry, and
general web search first; Apollo organization enrich only when free sources don't surface a
usable staff count, domain, or category. Apollo calls at the company level are cheaper than
per-person lookups and don't require the same row-by-row confirmation gate — the
confirmation gate in this spec is specifically about paid *contact/email* lookups, not
company enrichment. Still prefer free sources first to conserve credits either way.
