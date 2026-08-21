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

_No runs yet. The first run has no prior window; use the prior 7 days and record a full
pricing snapshot so later runs have a baseline to diff against._
