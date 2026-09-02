# Pushing to Attio (only after Austin's confirmation)

This step never runs automatically. It happens in a separate turn, after Austin has
reviewed `state/lists/healthcare-prospects-YYYY-MM-DD.xlsx`, resolved every `Unclear` and
`Flagged` row, and told the agent which rows to push (e.g. "push everything except rows 4
and 9" or "push all confirmed rows").

## Field mapping (verified against this workspace)

These slugs were pulled directly from `list-attribute-definitions` on the `companies` and
`people` objects in this Attio workspace, so they're not assumptions from the spec — they
match what's actually configured here.

**Companies** (`companies` object): `name`, `domains` (multiselect), `employee_range`
(select — see bucket list in `spreadsheet-schema.md`), `primary_location` (location type),
`categories` (multiselect, see categories gap note below), `linkedin`, `description`
(carries the Independence Flag Notes for `Unclear` rows that Austin confirmed as good).

**People** (`people` object): `name` (personal-name type), `job_title`, `email_addresses`
(multiselect), `phone_numbers` (multiselect), `linkedin`, `primary_location`, `company`
(record-reference to `companies` — this is what links a person to their company).

## Push order

1. **Companies first.** For each confirmed company row, check `Attio Status`:
   - `Already in Attio` → skip creation, but confirm the domain match still points to the
     record noted during dedupe (re-check by domain if the sheet is more than a few days
     old — records can change between list-build and push).
   - `New` → create the company record with the mapped fields above.
2. **People second**, linked to the company record created or matched in step 1. Use
   `company` as a record-reference to the company's Attio record ID, not just the name
   string — look up the record ID from the creation response (new companies) or from the
   dedupe check (existing companies).
   - `Already in Attio` → skip creation; optionally update fields that are new (e.g. an
     email the existing record didn't have) if Austin asked for updates, not just adds.
   - `New` → create the person record.

## Categories gap

The workspace's `categories` select has no general-practice healthcare option (see
`spreadsheet-schema.md`). Don't invent a mapping under time pressure — push with
`categories` left empty for these rows and tell Austin in the push summary that a workspace
option is needed if he wants these categorized going forward.

## Confirming before every push

Creating and linking CRM records is not reversible in the low-friction way a spreadsheet
edit is (merges and cleanup are real work later). Before calling any Attio create tool:
- State exactly which rows are being pushed (count of companies, count of people).
- Get Austin's explicit go-ahead in that turn, even if he already said "push it" once about
  the spreadsheet in general — confirm the final row set, especially if any rows changed
  between the review and the push (re-reading the file is expensive; asking is cheap).

## After the push

Report back: how many companies created vs. matched-existing, how many people created vs.
matched-existing, and any row that failed to push (with the reason) so it can be retried or
fixed by hand.
