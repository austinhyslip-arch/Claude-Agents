# Qualification — size and independence

Two separate checks. Size is a number; independence is a judgment call with three possible
outcomes (pass, excluded, unclear).

## Size check

- Target: under 200 staff, any specialty.
- Record the actual estimated count Austin sees in the spreadsheet — not a bucket. Sources
  in order: company's own "about" or careers page, LinkedIn company page employee count,
  Apollo organization enrich (`estimated_num_employees`), NPI Registry provider count for
  the practice (rough proxy — count of individual NPIs tied to the group NPI), press
  coverage mentioning staff size.
- If sources disagree, use the most recent and most specific one and note the conflict in
  the row (e.g. "LinkedIn shows 140, Apollo shows 210 — used LinkedIn, more recent").
- No number found anywhere → still include the row, count blank, `Size Check` = `Borderline`,
  and say in the notes what was tried.
- Map to Attio's bucket for the `Employee Range` column: 1-10, 11-50, 51-250, 251-1K, 1K-5K,
  5K-10K, 10K-50K, 50K-100K, 100K+. Anything in the 150-250 count lands in the 51-250 bucket
  in Attio even though it straddles the 200 cutoff — this is exactly why the precise count
  column exists. `Size Check` values:
  - `Pass` — confidently under 200
  - `Borderline` — count falls 150-250, or no confident number found
  - `Fail` — confidently 200+ (drop the row entirely, don't add it to the sheet)

## Independence check (exclusion filter)

Large healthcare systems and hospital chains absorb independent practices constantly. A
practice that's been rolled into HCA, Ascension, a regional health system, or a
private-equity-backed dental/vision/PT/dermatology chain is not a fit — Chanty's ICP here is
the owner-operator practice, not a location inside a larger org's IT stack.

**"Large corporation" means a large healthcare system or chain specifically** — a practice
owned by an unrelated non-healthcare holding company, or by an individual who owns two or
three clinics, is not what this filter is for. Don't exclude on general "has an owner"
grounds.

### Signals to check, in order (cheapest first)

1. **Website language.** Look at the practice's own site — header/footer, "About," "Our
   Story." Phrases like "part of," "a member of," "an affiliate of," "proud to be part of the
   [X] family," or a shared systemwide nav bar linking to a hospital system's main site are
   strong signals.
2. **Naming pattern.** Does the practice name itself match a known system/chain, exactly or
   as "[System Name] — [Location]" or "[System Name] [Specialty] of [City]"? Check
   `../state/known-health-systems.md` first — it's the running list of confirmed large
   systems/chains from prior runs. If the name pattern-matches something not yet on that
   list, treat it as a new candidate: verify with one search, and if confirmed, add it to the
   state file so future runs catch it without a fresh search.
3. **Apollo parent company field.** When Apollo enrichment returns a populated parent
   organization, check whether that parent is a large health system/chain (cross-reference
   `known-health-systems.md`) or something unrelated (a generic holding company, an
   individual owner's LLC, a franchisor of a non-healthcare business). Only the former
   excludes.
4. **Recent M&A news.** One search for "`<practice name>` acquired" or "`<practice name>`
   joins" — recent (last 3 years) acquisition by a system/chain is disqualifying even if the
   website hasn't caught up yet.

### Outcomes

- **Confirmed independent** (no signal fires) → include normally, `Independence Check`
  column left blank.
- **Confirmed part of a large system/chain** → exclude before the row is ever written to the
  spreadsheet. Austin never sees these. Log the exclusion in the run's entry in
  `../state/run-log.md` (name + which signal fired) so the count of candidates-considered vs.
  candidates-shown is auditable, but the company itself does not appear in the deliverable
  file.
- **Genuinely unclear** (signals conflict, or nothing found either way after checking all
  four) → include the row, `Independence Check` = `Unclear — needs manual check`, and note
  what was checked and why it didn't resolve. This is the one case where ambiguity goes to
  Austin instead of being silently resolved either direction.

### Maintaining `known-health-systems.md`

Every run that confirms a new large system or chain (via signal 2, 3, or 4) adds it to that
file if it isn't already there. This is a living list — the goal is that after enough runs,
most independence checks resolve on signal 2 (naming pattern) alone without needing a search.
