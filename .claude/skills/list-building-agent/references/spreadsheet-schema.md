# Spreadsheet schema

One `.xlsx` file per run, built with the `xlsx` skill. Two sheets: `Companies` and
`Contacts`, plus a third `Summary` sheet with run metadata (date, search criteria used,
counts: companies considered / excluded / included, contacts found, rows needing paid
lookup). Columns below mirror Attio's schema so a confirmed row maps 1:1 when it's pushed.

Field slugs were confirmed directly against this workspace's Attio object definitions
(`companies` and `people` objects) — see `attio-push.md` for the verification note and what
to do if the workspace schema changes.

## Companies sheet

| Column | Attio field (api_slug) | Notes |
|---|---|---|
| Company Name | `name` | |
| Domain | `domains` | |
| Estimated Staff Count (precise) | *(custom — not pushed directly)* | Used to pick the `employee_range` bucket on push; kept visible so Austin can eyeball 150-250 rows. |
| Employee Range (Attio bucket) | `employee_range` | One of: 1-10, 11-50, 51-250, 251-1K, 1K-5K, 5K-10K, 10K-50K, 50K-100K, 100K+. |
| Primary Location | `primary_location` | City/state is enough; full address if the source has it. |
| Category | `categories` | See the note below — the Attio workspace has no generic "Healthcare"/"Medical Practice" option today. |
| LinkedIn | `linkedin` | Company page URL. |
| Independence Flag Notes | *(custom — written to `description` on push)* | Only populated for `Unclear` rows; blank otherwise. |
| Size Check | *(review-only, not pushed)* | Pass / Borderline / Fail. Fail rows are dropped before the sheet is built, so this column should only ever show Pass or Borderline. |
| Independence Check | *(review-only, not pushed)* | Blank, or `Unclear — needs manual check`. Excluded companies never appear as rows. |
| Attio Status | *(review-only, not pushed)* | New / Already in Attio. |

### Categories gap

Checked this workspace's `categories` select options directly: the list is generic business
categories (Alternative Medicine, Construction, Education, Retail, Veterinary, etc.) and has
**no option for general medical/dental/vision/PT practices** — the exact verticals this spec
targets. Until Austin adds workspace options (or picks a stand-in), leave `Category` blank
in the sheet rather than force-fitting "Alternative Medicine" onto a family medicine
practice. Flag this in the run's `Summary` sheet so it doesn't get silently lost.

## Contacts sheet

| Column | Attio field (api_slug) | Notes |
|---|---|---|
| Full Name | `name` | |
| Job Title | `job_title` | Exact title as found, even for flagged/fuzzy matches. |
| Email | `email_addresses` | Verified or best guess — see `Email Source`. |
| Phone | `phone_numbers` | |
| LinkedIn | `linkedin` | Personal profile URL. |
| Primary Location | `primary_location` | Usually same as the company's; use the person's own if known to differ. |
| Company (linked) | `company` | Must match a row on the Companies sheet by name — used to link on push. |
| Title Match | *(review-only, not pushed)* | Matched / Flagged — unclear title. |
| Attio Status | *(review-only, not pushed)* | New / Already in Attio. |
| Email Source | *(review-only, not pushed)* | Verified (free source) / Guessed / Needs Paid Tool. |
| Email Guess Confidence | *(review-only, not pushed)* | e.g. "90% — pattern confirmed"; blank if verified. |
| Needs Paid Tool (Email) | *(review-only, not pushed)* | Yes / No. |

## Row order and formatting

- Group Contacts by company, in the same order the companies appear on the Companies sheet.
- Freeze the header row on both sheets.
- Highlight (light yellow fill) any row where `Independence Check` = `Unclear` or
  `Title Match` = `Flagged`, so Austin can scan for open items without reading every row.
- File name: `state/lists/healthcare-prospects-YYYY-MM-DD.xlsx`.
