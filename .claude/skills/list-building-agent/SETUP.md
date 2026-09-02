# Setup and operating notes

## How the agent gets invoked

On-demand only, in any session where this repo is checked out — no scheduled Routine is
part of this spec (lists are generated when Austin asks, not on a fixed cadence). Ask for a
list ("build me a list of independent dental practices in Texas under 200 staff") and it
runs `SKILL.md` end to end through the spreadsheet, then stops.

## Dependencies at run time

| Dependency | Status | Notes |
|---|---|---|
| Web search (built-in) | Available | Stands in for "Google Custom Search API" from the original spec — no Custom Search API key is configured in this environment. If Austin provides one later, wire it in and update `references/sourcing.md`. |
| NPI Registry (NPPES) direct API | **Blocked** | Tested directly (`npiregistry.cms.hhs.gov`) during this skill's build — refused by the network egress policy. Fall back to web search for NPI lookups until this is retested in an environment with open egress. |
| Facebook business pages | Untested | Not verified reachable in this environment; if fetches are blocked, fall back to web search results that surface the same page content. |
| Apollo.io | Connected (MCP) | Used for company-search fallback, organization enrich (staff count, parent-company signal), and person match/enrich for the confirmed paid-lookup step. |
| Hunter.io | **Not connected** | No Hunter MCP server is available in this environment as of this skill's build. Apollo is the only paid contact-enrichment tool actually usable right now — treat Hunter steps in the spec as aspirational until it's connected. |
| Attio | Connected (MCP) | Verified: `companies` and `people` object schemas pulled directly and match the spec's field slugs (`name`, `domains`, `employee_range`, `primary_location`, `categories`, `linkedin`, `description` on companies; `name`, `job_title`, `email_addresses`, `phone_numbers`, `linkedin`, `primary_location`, `company` on people). One gap found: the `categories` select has no general medical/dental/vision/PT practice option — see `references/spreadsheet-schema.md`. Used for dedupe reads always; used for writes only after Austin's explicit confirmation. |
| `xlsx` skill | Available | Used to build the review spreadsheet. |
| Google Drive / Gmail | Connected (MCP) | Not required by this workflow's core loop; available if Austin wants the spreadsheet delivered by email or Drive link instead of (or in addition to) the in-session file send. |

## Verifying the Attio field mapping stays current

The mapping in `references/spreadsheet-schema.md` and `references/attio-push.md` was
pulled directly from `mcp__Attio__list-attribute-definitions` on the `companies` and
`people` objects, not copied from the original spec unchecked. If a push fails on a field
name, re-run `list-attribute-definitions` for the relevant object before assuming the
workflow logic is wrong — the workspace schema may have changed (a renamed slug, a new
required field, a changed select option list).

## `employee_range` bucket confirmation

Confirmed directly: 1-10, 11-50, **51-250**, 251-1K, 1K-5K, 5K-10K, 10K-50K, 50K-100K,
100K+. The spec's concern is accurate — 51-250 really does straddle the 200-staff cutoff,
which is why the spreadsheet carries a precise headcount column alongside the bucket.

## State and git

`state/run-log.md`, `state/known-health-systems.md`, and `state/lists/` are the agent's
memory and archive. A run that builds the spreadsheet but leaves state uncommitted loses
the exclusion list's growth and the market-coverage history for the next run — commit at
the end of every run, per step 11 in `SKILL.md`.
