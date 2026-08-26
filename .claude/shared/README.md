# Shared files between Chanty agents

Files here are written by one agent and read by another. Each one is a contract: change the
shape and you break the reader.

## `content-gaps.json`

**Written by** `chanty-competitive-intel` → `scripts/search_demand.py`, weekly.
**Read by** the content idea agent, for its trend-jacking and comparison categories.

Every search term with a usable SERP produces one entry per week. An entry says who ranks
for a switching-intent term and where Chanty sits, so a gap becomes a content idea without
anyone having to spot it first.

```json
{
  "source": "chanty-competitive-intel/search-demand",
  "updated": "2026-08-24T13:04:11Z",
  "entries": [
    {
      "week": "2026-08-24",
      "term": "cheaper than slack",
      "tier": 2,
      "set": "slack",
      "category": "gap",
      "chanty_rank": null,
      "trend": "up",
      "top_domains": [
        { "rank": 1, "domain": "pumble.com", "title": "…", "link": "https://…" }
      ],
      "note": "Chanty is not in the top 10 for \"cheaper than slack\"; pumble.com, flock.com, zoho.com are."
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `week` | ISO date of the run. A rerun for the same week replaces that week's entries. |
| `tier` | 1 active switching intent · 2 price sensitivity · 3 comparison · 4 brand. Lower is more urgent. |
| `set` | Which competitor keyword set produced the term (`slack`, `teams`, `google_chat`, or `_global`). |
| `category` | `comparison` for head-to-heads, `trend-jacking` for a rising term Chanty is absent from, `gap` otherwise. |
| `chanty_rank` | 1-based rank in the top 10, or `null` when Chanty does not appear. `null` on a Tier 1 or 2 term is the finding. |
| `trend` | `up` · `flat` · `down` · `unavailable`. |
| `top_domains` | Top 5 results, with links. |
| `note` | The finding as one sentence, ready to read. |

**Reader notes.** The file is cumulative, newest entries appended — filter by `week` for
this week's ideas. Treat a missing `trend` (`unavailable`) as unknown, not as flat. An
entry is a signal, not an assignment: rank and tier say how much it is worth.

Definitions of the terms and tiers:
`.claude/skills/chanty-competitive-intel/references/search-demand.md`.
