# Run log

Append one entry per run, newest at the top. This is the dedupe memory — the next run
reads it to avoid re-reporting the same acquisition three weeks running, and to know the
default window for an on-demand check.

Entry format:

```
## YYYY-MM-DD — [Weekly | On-Demand | + Discovery]
Window: YYYY-MM-DD to YYYY-MM-DD
Sent: yes / no (reason)

Big Stuff reported:
- <Competitor> — <one line> [url]

Pricing snapshot (Tier 1 + Tier 2, per-seat monthly where published):
- <Competitor>: <plan> $X, <plan> $Y

Notes: <anything the next run needs — a source that moved, a thread still developing>
```

---

## 2026-08-21 — On-Demand (send test)
Window: 2026-08-07 to 2026-08-21
Sent: yes (Gmail message id 1a0260c7944aa083)

Big Stuff reported:
- Notion — AI usage credits on Business/Enterprise, full AI gated to Business $20+ [eesel.ai, flowith.io]
- monday.com — Q2 2026 results Aug 10, rev $364.6M +22%, ARR $1.5B, stock -12% on guidance; NDR pressure from prior pricing actions [ir.monday.com]
- monday.com — "20% workforce reduction" claim, SINGLE SOURCE, unconfirmed [investing.com]
- Slack — outages Aug 13 and Aug 21 (16h warning), 5 incidents in 30 days [statusgator]
- Asana — CAO Veronica Sosa resignation effective Aug 7; Q2 FY27 earnings Sept 3 [TipRanks]

Pricing snapshot (per seat / month, secondary sources only this run):
- Slack: Pro $7.25, Business+ $15
- Microsoft: Teams Essentials $4, Teams Enterprise $8.55, M365 Business Basic $7, Standard $14
- ClickUp: Unlimited $7, Business $12 (annual); Brain $9, Everything AI $28
- Notion: Plus $10, Business $20

Notes: Send path verified end to end. Egress policy blocked direct loads of slack.com,
notion.com, clickup.com, basecamp.com, g2.com and capterra.com — no G2/Capterra review
harvest happened, and the pricing snapshot is secondary-sourced, below the confirmation
bar this skill sets. Next run needs open egress before the pricing diff means anything.
Chanty: no new mentions in window.

---

_No runs yet. The first run has no prior window; use the prior 7 days and record a full
pricing snapshot so later runs have a baseline to diff against._
