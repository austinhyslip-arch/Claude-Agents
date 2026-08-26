---
name: chanty-competitive-intel
description: Competitive monitoring for Chanty across team chat, task management, and combined-workspace tools. Use for the Monday weekly competitive digest, an on-demand competitive check ("run a competitive check", "what has Slack shipped this week", "anything new from Monday.com"), or the monthly Tier 3 discovery pass. Gathers pricing changes, launches, funding, acquisitions, outages, leadership changes and layoffs, plus recurring pricing and feature complaints from G2, Capterra, Reddit, Hacker News, changelogs and pricing pages, tracks weekly search demand for switching-intent terms (Slack/Teams alternatives, pricing complaints) with Google Trends and the Custom Search API, builds the briefing as a styled HTML file, and emails it to austinhyslip@gmail.com as an attachment. Does not write to Attio.
---

# Chanty Competitive Intelligence

Track every platform competing with Chanty for team chat, task management, or combined
workspace budget. Surface major moves fast; compile pricing and feature complaints into a
weekly digest so marketing and sales know where competitors are weak.

Output is research only. **This agent never writes to Attio or any CRM.**

## Run modes

| Mode | When | Window | Run type |
|---|---|---|---|
| Weekly | Mondays, 8:00am Central | Prior 7 days | `Weekly` |
| On-demand | Whenever Austin asks — daily is fine | Whatever he names; default = since the last entry in `state/run-log.md` | `On-Demand` |
| Discovery | Folded into whichever digest lands closest to the 1st | Prior 30 days | Adds ` + Discovery` |

Every run ends with one email to **austinhyslip@gmail.com** carrying the briefing as an
HTML attachment. Big Stuff flags appear at the top of the attachment and as headline
bullets in the short email body, never buried under review complaints.

### Scheduling and daylight saving

The weekly digest is due **08:00 America/Chicago**. If the scheduler accepts a timezone,
set Central directly and ignore the rest of this. Claude Code Routines take **cron in UTC
only**, so the correct expression changes twice a year:

| Period | Central | Cron (UTC) |
|---|---|---|
| CDT — second Sunday of March to first Sunday of November | UTC−5 | `0 13 * * 1` |
| CST — first Sunday of November to second Sunday of March | UTC−6 | `0 14 * * 1` |

Next switches: **Nov 1, 2026** (→ `0 14 * * 1`) and **Mar 14, 2027** (→ `0 13 * * 1`).

On every weekly run, check whether the firing time still lands at 08:00 Central. If it has
drifted an hour, say so in the run summary and tell Austin which cron to set — the agent
cannot assume it has permission to rewrite its own schedule.

## Workflow

### 1. Set the window and load state
- Read `state/run-log.md` for the last run date and the items already reported.
- Read `state/tier3-candidates.md` for the live Tier 3 list.
- Determine whether this run also carries the discovery pass (nearest digest to the 1st, or
  no discovery entry in the run log within the last 30 days).

### 2. Big Stuff sweep — all Tier 1 and Tier 2, every run
For each competitor in `references/watchlist.md`, check the six flag categories in
`references/signal-rubric.md`: pricing change, major launch or product acquisition,
funding / M&A, outage or security incident, C-suite change, layoffs or restructuring.

Work the cheap sources first — changelog and pricing page for the product's own moves, then
news search for company-level moves. Tier 3 gets a single combined news search per name.

### 3. Complaint harvest
Pull G2 and Capterra reviews from inside the window plus relevant Reddit and Hacker News
threads, per `references/sources.md`. Group by competitor, split into **pricing** and
**feature** complaints. A complaint earns a line when it appears **twice or more** in the
window, or once if it is unusually specific and sales-usable (a named unexpected charge, a
hard seat minimum, a removed feature).

### 4. Chanty mentions
Search for Chanty across the same sources. Report praise, criticism, and any head-to-head
comparison. If nothing turns up, say so in one line — do not pad it.

### 5. Search demand signals — weekly runs
Run the switching-intent pull, per `references/search-demand.md`:

```bash
python3 scripts/search_demand.py
```

It writes `state/search-demand/<week>.section.html` — paste that fragment whole into the
digest at `#search-demand` — plus a full snapshot, the SERP history, and gap findings in
`.claude/shared/content-gaps.json` for the content idea agent. It never raises into the
build: a dead source becomes a visible gap in a row. Read its stderr and carry any
whole-source failure into `{{CAVEATS}}`. Skip this step on on-demand runs; the data does
not move fast enough to be worth a second pull inside a week.

### 6. Discovery pass (monthly)
Run the four discovery queries in `references/sources.md` across G2, Capterra and general
web search. Any product name appearing in **two or more distinct sources** is added to Tier
3 in `state/tier3-candidates.md` with its first-seen date and the sources that surfaced it.
Names already tracked get their last-seen date refreshed. A tracked name with no appearances
across three consecutive passes moves to `dormant` — keep the row, stop searching it.

### 7. Score
Apply `references/signal-rubric.md` to separate Big Stuff from noise. Report at 4+.

### 8. Build the briefing
Build the HTML file from `references/digest-template.html` following
`references/digest-format.md`. Save it to `state/digests/chanty-competitive-briefing-YYYY-MM-DD.html`.

Before sending, verify the file: no `{{TOKENS}}` left unsubstituted, no `data-sample`
elements surviving, no empty sections, every item carrying a source link and date.

### 9. Send
Email **austinhyslip@gmail.com** with the HTML file **attached** and a short body — one
line on what is attached, plus the Big Stuff headlines as bullets when there are any.
Subject line per `references/digest-format.md`.

The attachment is the point: Gmail's renderer breaks the stamps, borders and paper ground
this design depends on. If the session's Gmail tool cannot attach a file, follow the
fallback chain in `digest-format.md` — Drive link first, inline plain text second — and say
in the body which path was used and why.

### 10. Update state
Append this run to `state/run-log.md`: window, every Big Stuff item with its URL, the
pricing snapshot, the search-demand line (terms pulled, terms shown, any source that
failed), the send path used, and the digest filename. Commit the run log, the
digest file, the search-demand snapshot and cache, the SERP history, the shared content-gap
file, and any Tier 3 changes. The run log is what stops the next run from
re-reporting the same acquisition three weeks running.

## Rules that keep the digest trustworthy

- **Every item carries a source URL and a date.** No URL, no item.
- **Two-source rule for money and ownership.** Funding, acquisitions, layoffs and revenue
  claims need two independent sources, or one primary source (the company's own post, a
  filing, a named-reporter story). A single Reddit comment is a lead, not a finding — if it
  ships at all, it ships under the `Unconfirmed` stamp.
- **Pricing changes get verified against the live pricing page**, not someone's
  recollection of it. Quote old and new numbers when both are known. If the page could not
  be reached, say so in `{{CAVEATS}}` rather than passing a blog's number off as verified.
- **One to two sentences per item.** Scan-in-two-minutes, not a thread summary.
- **Do not re-report.** Skip anything already in `state/run-log.md` unless it materially
  escalated (rumor → confirmed, price floated → price live).
- **Quote fragments, don't paste reviews.** Twenty words max from any single review.
- **"Users report" and "Slack announced" are different claims.** Keep them different.
- **A missing search-demand source is stated, never hidden.** "Trends data unavailable
  this week" in a row is a working digest; a row quietly dropped because the pull failed
  is not.
- **Never contact a competitor, sign up under false pretenses, or scrape behind a login.**

## Adapting the outbound scoring logic

If `outbound-triggers-6` or `outreach-4-categories` are installed, read them first and use
their thresholds for trigger versus noise — this agent borrows that logic rather than
inventing a parallel one. `references/signal-rubric.md` is the standalone fallback. Use the
`research` skill for source gathering and synthesis when it is available.

## Files

- `references/watchlist.md` — tiers, and the canonical pricing / changelog / blog / status
  URL for each tracked competitor
- `references/sources.md` — per-source query patterns and filters
- `references/signal-rubric.md` — Big Stuff vs. noise scoring
- `references/digest-format.md` — how the HTML file is filled, subject lines, email body,
  and the send fallback chain
- `references/search-demand.md` — the Search Demand Signals section: taxonomy, sources,
  what earns a row, failure behaviour, and the content-gap handoff
- `references/search-terms.json` — the search term taxonomy, tiered and templated
- `references/digest-template.html` — the briefing template itself
- `state/tier3-candidates.md` — live Tier 3 list, maintained by the discovery pass
- `state/run-log.md` — what has already been reported
- `state/digests/` — every briefing this agent has produced
- `state/search-demand/` — weekly search-demand snapshots and HTML fragments
- `state/serp-history.jsonl` — SERP results by term and week, for the long view
- `scripts/` — the search-demand pipeline and its offline self-test
- `../../shared/content-gaps.json` — gap findings handed to the content idea agent
