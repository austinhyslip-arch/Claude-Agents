# Vertical Sourcing Agent: Manufacturing and Municipal

## What this agent does

Sources 20 qualified accounts per vertical per run, nationwide. Runs every weekday. Company-level records only. No contact names, no personal emails, no people enrichment. Output goes to an HTML email digest and is pushed to Attio automatically.

Per run: 40 accounts, 20 per vertical.
Per week: 200 accounts.

This is a sourcing agent only. It does not write or send outreach. Copywriting and sending stay with the existing outbound agents.

## Note on the Attio push

The healthcare agent requires Austin's confirmation before any Attio push. This agent does not. Records that pass all qualification filters are written to Attio on the same run that produces the digest. Records that are ambiguous are held back and listed in a review section of the email instead. See "Review gate" below.

## Note on paid tools

No paid credits are spent by this agent. Apollo may be used for information available on its free tier only. Hunter and Clay are not used at all, since no contact-level enrichment happens here. If a record cannot be completed from free sources, it goes to the review section rather than triggering a paid lookup.

---

## Vertical 1: Small municipalities and special districts

### ICP

| Criterion | Rule |
|---|---|
| Entity type | Cities, towns, villages, and special districts |
| Special district types in scope | Water and sewer, fire protection, parks and recreation, irrigation, port, transit, utility, library, hospital district |
| Employees | 75 or fewer. This is a hard cap |
| Population proxy | 2,500 to 20,000 for municipalities, used only when a staff count cannot be found |
| Geography | United States, all states |

### The 75 employee cap

This is the gating filter, not population. Population is a fallback.

1. Look up the entity in the **Census Bureau Annual Survey of Public Employment and Payroll (ASPEP)**, which publishes full-time and part-time employee counts per individual government unit. Use full-time equivalent where given.
2. If ASPEP has the entity and FTE is above 75, exclude it. No further checking.
3. If ASPEP does not carry it, fall back to the population band above.
4. If population is also unavailable, send the record to review rather than guessing.

Write both `staff_count` and `staff_count_source` on every record so the accuracy of the fallback can be checked later.

### Exclusions

- Any entity with more than 75 employees.
- Counties. Different structure and a much longer procurement cycle.
- School districts. Different buyer and a different budget cycle. Hold for a separate test.
- State agencies, federal agencies, tribal governments.
- Municipalities under 2,500 population. Too few employees to justify a seat purchase.
- Any entity whose domain already exists in Attio.

### Sourcing waterfall

1. **CISA .gov domain registry** (`https://github.com/cisagov/dotgov-data`). Public CSV of every registered .gov domain with organization name, state, and entity type. This is the primary seed. Filter to City, Town, Village, and Special District rows.
2. **Census ASPEP** for employee counts, and **Census population data** as the fallback size proxy.
3. **State special district registries** for districts that do not hold a .gov domain. Most states publish one. Examples: Texas Comptroller special purpose district list, Florida Special District Accountability Program, Colorado DOLA, California State Controller.
4. **Google Custom Search API** to find the entity website and the main phone number where the registry does not carry it.

### Phone number rule

Main line only. Pull the general administrative number listed on a City Hall, Administration, or Clerk page. Do not pull police non-emergency lines, 911 lines, or a named individual's direct dial. If only a switchboard number is available, take it and note the source.

---

## Vertical 2: Light manufacturing and distribution

### ICP

| Criterion | Rule |
|---|---|
| Industry | NAICS 31, 32, 33. Also 4931 and 4885 for third party logistics and warehousing |
| Employees | 50 to 250 |
| Locations | 1 to 3 facilities |
| Ownership | Independent. Not a division or subsidiary of a larger parent |
| Geography | United States, all states |

Preferred subsegments where the deskless problem is sharpest: food processing, plastics and rubber, metal fabrication, building products, contract packaging, furniture, printing.

### Exclusions

- Publicly traded companies.
- Subsidiaries, divisions, and plants of a parent company with more than 500 total employees. Independence matters as much as headcount, same rule as the healthcare ICP.
- Under 50 or over 250 employees.
- Pure holding companies and pure distributors with no warehouse staff.
- Any domain already in Attio.

### Sourcing waterfall

1. **Google Custom Search API** against state manufacturing association member directories. Every state has one and most publish members publicly. Search pattern: `"[state] manufacturers association" member directory`.
2. **ThomasNet and public supplier directories** for company name, location, and main phone.
3. **Apollo free tier** to fill in headcount band and company phone where steps 1 and 2 came up short. Free information only. Do not consume credits.
4. If a record is still incomplete, send it to review. Do not escalate to a paid source.

### Phone number rule

Main company line only, the number on the contact page or the directory listing. No direct dials.

### Headcount handling

Attio's `employee_range` bucketed field can be written as is for this vertical. Also write a separate precise `staff_count` column with the actual number found, plus `staff_count_source` noting where it came from. If no precise number is available, estimate from the directory listing and mark it as an estimate.

---

## Record schema

Both verticals write the same shape.

| Field | Notes |
|---|---|
| `company_name` | Legal or common name |
| `domain` | Primary website domain, normalized, no protocol and no www |
| `city` | |
| `state` | Two letter |
| `phone` | Main line, E.164 format |
| `vertical` | `manufacturing` or `municipal` |
| `subsegment` | e.g. `food processing`, `water district` |
| `staff_count` | Integer where known |
| `staff_count_source` | `aspep`, `directory`, `apollo_free`, `estimate` |
| `population` | Municipal records only |
| `source` | Which step of the waterfall produced it |
| `sourced_date` | ISO date |
| `qualification_note` | One line on why it passed |

## Deduplication

Daily runs put real pressure on dedupe. Check before any record is written:

1. Normalize the domain. Strip protocol, www, and trailing slash.
2. Query Attio for an existing company with that domain.
3. If no domain match, fuzzy match on normalized company name plus state.
4. Maintain a local seen-entities file across runs so the same directory page does not get re-scraped into the same candidates every morning.
5. Skip on match. Count skips and report them in the digest summary.
6. Dedupe within the run as well, since the same company can surface from two directories.

### Pool tracking

Log how much of each source pool has been consumed. The municipal pool is finite once the 75 employee cap is applied. When a vertical drops below roughly 500 unseen candidates, say so in the digest so the ICP can be widened before the well runs dry.

## Attio push

Create two company-based lists, matching the existing naming convention:

- `Manufacturing / US / Agent`
- `Municipal / US / Agent`

Push happens on the same run as the digest, but **after** the digest has been sent. Never let a slow or failing Attio write delay the 9:00am email. If the push fails or partially fails, retry twice, then log the failed records and report them at the top of the next morning's digest so they can be pushed on the following run.

Write all schema fields. Set pipeline stage to the earliest sourced stage. Do not set any stage past initial sourcing, and never write a contracting or later stage.

### Review gate

A record is held back from Attio and listed in a "Needs review" section of the email if any of the following are true:

- Employee count could not be determined and no population fallback exists.
- Ownership independence is unclear for a manufacturer.
- The entity type is ambiguous, for example a district that may be a school district.
- No main phone number could be found from free sources.
- Two candidate records look like the same organization but could not be confidently merged.

Held records are not pushed on a later run automatically. Austin either adds them by hand or tells the agent to release them.

## Email digest

Send to austinhyslip@gmail.com.

Gmail strips CSS from email bodies, so build the digest as an HTML file and attach it. Keep the email body to a plain text summary line.

Digest contents:

1. Summary. Counts per vertical, duplicates skipped, records held for review, any source that failed.
2. Manufacturing table. Company, city and state, phone, staff count, subsegment.
3. Municipal table. Entity, city and state, phone, staff count, district type.
4. Needs review section with the reason per record.
5. Source health. Which directories returned results and which returned nothing, plus remaining pool estimates.

## Schedule and delivery guarantee

**The digest must be in the inbox by 9:00am Central every weekday. This is the hard requirement everything else is built around.** A late list is worse than a short list. If the agent has to choose between hitting 20 records and hitting 9:00am, it hits 9:00am.

Set all cron timing in the `America/Chicago` timezone, not a fixed UTC offset, so daylight saving shifts do not move the run.

### Daily timeline

| Time (Central) | What happens |
|---|---|
| 6:00am | Primary run starts. Loads cached registry files, begins sourcing both verticals |
| 7:00am | Retry window. If the 6:00am run failed to start or crashed, it runs once more here |
| 7:30am | **Soft checkpoint.** Stop opening new sources. Finish and qualify whatever is already in flight |
| 8:15am | **Hard stop.** Abandon anything unfinished. Qualify what exists, build the digest |
| 8:30am | Digest sent. Attio push begins after the send, not before |
| 8:45am | **Failure alarm.** If no digest has gone out, send a plain text email saying the run failed and why |

### Checkpoint behavior

At 7:30am the agent stops looking for new candidates and works only with what it already has. Partial records that cannot be completed by the hard stop go straight to the review section rather than holding up the send.

At 8:15am the agent finalizes no matter what state it is in. A run that produces 11 manufacturing records and 20 municipal records still sends at 8:30am with the shortfall stated at the top of the digest.

### Never block the morning window

Nothing slow or optional runs between 6:00am and 9:00am:

- Monthly registry file refreshes run Sunday at 8:00pm Central, never inside the morning window.
- Pool tracking and log rotation run after the digest is sent, not before.
- The Attio push runs after the digest is sent. See below.

### Heartbeat

Every run writes a completion record with the send timestamp. If two consecutive weekdays pass with no successful send, escalate with a separate alert email so a silent failure does not go unnoticed for a week.

## Rate limits and failure handling

Daily runs make the Google Custom Search quota the binding constraint. Budget accordingly.

- Google Custom Search API free tier is 100 queries per day. Cap spend at roughly 2 queries per record and stop cleanly at the quota rather than erroring out.
- Cache the CISA .gov CSV, the ASPEP file, and Census population data locally. Refresh monthly on a Sunday at 8:00pm Central, never inside the morning window and never per run.
- Cache scraped directory pages for 30 days so repeat runs pull from disk instead of burning queries.
- Retry any HTTP failure twice with backoff, then record the source as failed and continue. A single dead directory should never kill the run.
- If a vertical finishes with fewer than 20 qualified records, send the digest anyway with the shortfall stated. Do not lower the qualification bar to hit the number.

## Logging

Write a run log per execution with timestamp, records found per source, records qualified, records skipped as duplicates, records held for review, API calls consumed, and remaining pool estimate. Keep the last 30 runs.

## Success criteria

- Digest in the inbox before 9:00am Central on every weekday, without exception.
- 20 qualified records per vertical per weekday run.
- No municipal record with more than 75 employees reaches Attio.
- Under 5 percent duplicate rate against Attio after the first month.
- Main phone number present on at least 90 percent of pushed records.
- Zero paid credits consumed.
