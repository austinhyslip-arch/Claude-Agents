---
name: chanty-competitive-intel
description: Competitive monitoring for Chanty across team chat, task management, and combined-workspace tools. Use for the Monday weekly competitive digest, an on-demand competitive check ("run a competitive check", "what has Slack shipped this week", "anything new from Monday.com"), or the monthly Tier 3 discovery pass. Gathers pricing changes, launches, funding, acquisitions, outages, leadership changes and layoffs, plus recurring pricing and feature complaints from G2, Capterra, Reddit, Hacker News, changelogs and pricing pages, then emails the digest to austinhyslip@gmail.com. Does not write to Attio.
---

# Chanty Competitive Intelligence

Track every platform competing with Chanty for team chat, task management, or
combined workspace budget. Surface major moves fast; compile pricing and feature
complaints into a weekly digest so marketing and sales know where competitors are
weak.

Output is research only. **This agent never writes to Attio or any CRM.**

## Run modes

| Mode | Trigger | Window | Subject line |
|---|---|---|---|
| Weekly | Every Monday | Prior 7 days | `[Weekly] Competitive Digest — <Mon DD, YYYY>` |
| On-demand | Austin asks | Whatever he names; default = since the last entry in `state/run-log.md` | `[On-Demand] Competitive Check — <window>` |
| Discovery | Folded into whichever digest lands closest to the 1st | Prior 30 days | Append `+ Discovery` to that run's subject |

Every run — weekly or on-demand — ends with one email to **austinhyslip@gmail.com**.
Big Stuff flags go at the top of that email, above the complaint summary, never
buried underneath it.

## Workflow

### 1. Set the window and load state
- Read `state/run-log.md` for the last run date and the items already reported.
- Read `state/tier3-candidates.md` for the live Tier 3 list.
- Determine whether this run also carries the discovery pass (nearest digest to the 1st,
  or no discovery entry in the run log within the last 30 days).

### 2. Big Stuff sweep — all Tier 1 and Tier 2, every run
For each competitor in `references/watchlist.md`, check for the six flag categories in
`references/signal-rubric.md`: pricing change, major launch or product acquisition,
funding / M&A, outage or security incident, C-suite change, layoffs or restructuring.

Work the cheap sources first: changelog and pricing page for the product's own moves,
then news search for company-level moves. Tier 3 gets a single combined news search per
name, not a full per-source pass.

### 3. Complaint harvest
Pull G2 and Capterra reviews from inside the window plus relevant Reddit and Hacker News
threads, per `references/sources.md`. Group findings by competitor and split into
**pricing complaints** and **feature complaints**. A complaint earns a line in the digest
when it shows up **twice or more** in the window, or once if it is unusually specific and
sales-usable (a named unexpected charge, a hard seat minimum, a removed feature).

### 4. Chanty mentions
Search for Chanty by name across the same sources. Report praise, criticism, and any
head-to-head comparison where Chanty appears. If nothing turns up, say "No Chanty
mentions this window" — do not pad it.

### 5. Discovery pass (monthly)
Run the four discovery queries in `references/sources.md` across G2, Capterra and general
web search. Any product name appearing in **two or more distinct sources** gets added to
Tier 3 in `state/tier3-candidates.md` with its first-seen date and the sources that
surfaced it. Names already tracked just get their last-seen date refreshed. A tracked
Tier 3 name with no appearances for three consecutive discovery passes moves to
`dormant` — keep the row, stop searching it.

### 6. Score, then write
Apply `references/signal-rubric.md` to separate Big Stuff from noise. Then assemble the
email using `references/digest-format.md`.

### 7. Send
Send via the Gmail connector already set up for the outbound agent — same auth, no new
setup. Recipient: `austinhyslip@gmail.com`.

**If Gmail is unavailable in the session** (connector not enabled, auth expired): write the
digest to `state/digests/<YYYY-MM-DD>-<weekly|on-demand>.md`, tell Austin plainly that the
send failed and why, and hand him the file. Never silently drop a run.

### 8. Update state
Append this run to `state/run-log.md` (date, mode, window, every Big Stuff item reported
with its URL). Commit the state changes. The run log is what stops the next run from
re-reporting the same acquisition three weeks running.

## Rules that keep the digest trustworthy

- **Every item carries a source URL and a date.** No URL, no item — drop it rather than
  report it soft.
- **Two-source rule for money and ownership.** Funding rounds, acquisitions, layoffs and
  revenue claims need two independent sources, or one primary source (the company's own
  post, an SEC filing, a named-reporter story). A single Reddit comment is a lead, not a
  finding.
- **Pricing changes get verified against the live pricing page**, not against someone's
  recollection of it. Quote the old and new number when both are known.
- **One to two sentences per item.** This is a scan-in-two-minutes email, not a summary of
  every thread.
- **Do not re-report.** Skip anything already in `state/run-log.md` unless it materially
  escalated (rumor → confirmed, price floated → price live).
- **Quote fragments, don't paste reviews.** Twenty words max from any single review, with
  attribution to the platform and date.
- **No competitor speculation dressed as fact.** "Users report" and "Slack announced" are
  different claims; keep them different in the text.
- **Never contact a competitor, sign up under false pretenses, or scrape behind a login.**
  Public sources only.

## Adapting the outbound scoring logic

If the `outbound-triggers-6` or `outreach-4-categories` skills are installed, read them
first and use their thresholds for what counts as a real trigger versus noise — this agent
borrows that logic rather than inventing a parallel one. `references/signal-rubric.md`
carries a standalone version for when they are not available.

## Reference files

- `references/watchlist.md` — tiers, and the canonical pricing / changelog / blog / status
  URL for each tracked competitor
- `references/sources.md` — per-source query patterns and filters
- `references/signal-rubric.md` — Big Stuff vs. noise scoring
- `references/digest-format.md` — email structure and subject lines
- `state/tier3-candidates.md` — live Tier 3 list, maintained by the discovery pass
- `state/run-log.md` — what has already been reported
