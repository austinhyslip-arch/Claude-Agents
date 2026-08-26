# Search Demand Signals

Tracks people actively searching for a way off Slack, Teams, or Google Chat, and who is
winning the results for those terms. Switching intent is a stronger signal than a Reddit
mention or a G2 review: someone typing `cheaper than slack` has already decided to look.

The same pull doubles as content gap research — the SERP half shows who ranks and, by
subtraction, what Chanty isn't writing.

**This does not run standalone.** It adds one section to the Monday digest and writes gap
findings to a shared file the content idea agent reads.

## Term taxonomy

Terms live in `search-terms.json` and are generated from templates, so a term change or a
new competitor set is a config edit, not a code edit. `python3 scripts/search_terms.py`
prints the live list.

| Tier | Intent | What a hit means |
|---|---|---|
| 1 | Active switching | `slack alternatives`, `alternative to teams`, `slack vs <competitor>` — read these first |
| 2 | Price sensitivity | `cheaper than slack`, `free alternative to slack`, `slack alternative small business` |
| 3 | Comparison and evaluation | `what's better than slack`, `best team chat app <year>` |
| 4 | Brand tracking | `chanty vs slack`, `chanty reviews`, `is chanty good` — a check, not a headline |

Each set (Slack, Teams, Google Chat) runs the full tier list against its own product name.
`{target}` is the formal name (`microsoft teams`), `{short}` is how people type it
(`teams`); templates use whichever the real-world phrasing uses. Templates marked
`"scope": "global"` render once for the whole run, not once per set — `best team chat app
2026` is not a Slack term and a Teams term.

**Google Chat is defined and disabled.** Its set is in the config with `"enabled": false`.
Turning it on is that one flag; it adds ~13 terms to the weekly pull. See "Open decisions"
below for why it ships off.

## Sources

**Google Trends via pytrends** — interest over time and direction of movement. Unofficial:
it calls the same backend endpoints that power the trends.google.com explore page, because
Google blocks scraping the page itself. It breaks when Google changes that backend, and
rate-limits hard (429) when queried too fast. One weekly pull, one term per request, a
delay between requests, retries with backoff. Never a source of truth on its own.

**Google Custom Search API** — the SERP snapshot: who ranks in the top 10 for each term
right now. Official, stable, and the half that carries the section. Same API key as social
listening; the free tier is 100 queries/day and a full weekly run at both sets is 29.

## Cadence

Weekly, in the same run as the Monday digest. Trend data doesn't move enough day to day to
justify more, and weekly keeps the pytrends rate-limit risk low.

## Running it

```bash
export GOOGLE_CSE_API_KEY=...   # same credentials as social listening
export GOOGLE_CSE_CX=...
python3 scripts/search_demand.py                      # full weekly run
python3 scripts/search_demand.py --no-trends          # SERP only, no arrows
python3 scripts/search_demand.py --terms 4 --dry-run  # smoke test, writes nothing
python3 scripts/selftest.py                           # offline, after any script change
```

A full run takes roughly three minutes, nearly all of it the deliberate delay between
pytrends calls. It writes:

| Path | What |
|---|---|
| `state/search-demand/<week>.section.html` | the HTML fragment to paste into the digest |
| `state/search-demand/<week>.json` | every term pulled this week, quiet ones included |
| `state/search-demand-cache.json` | last good index and top 3 per term — powers the arrows |
| `state/serp-history.jsonl` | one line per term per week, the long view on ranking shifts |
| `.claude/shared/content-gaps.json` | gap findings for the content idea agent |

## What earns a row

A term is pulled every week. It is **shown** only when it has something to say:

- the trend moved 10% or more in either direction, or
- a domain entered or left the top 3, or
- Chanty entered or left the top 10, or
- the term has never been recorded before (one baseline sighting), or
- both its sources failed — a silent failure is the thing this section is least allowed to do.

Everything else is dropped from the digest rather than shipped as an empty box. It is still
pulled, cached and written to the snapshot; it just doesn't take a line. Rows sort by tier
first, then by whether Chanty's position moved, then by size of the move, capped at 12 so
the section stays one screen.

**Trend direction** compares this week's index against last week's cached value
(`week-over-week`). With no cached value — first run, or last week's pull failed — it falls
back to the last 14 days against the 14 before them (`prior-period`), so a cold start still
has arrows. Which basis was used is in the row's tooltip and in the JSON.

## Failure behaviour

Nothing here is allowed to fail the digest build.

- A pytrends failure writes **"Trends data unavailable this week"** into that row, in the
  caution gold, and the row still ships with its SERP data. The reason is printed to
  stderr and stored in the snapshot JSON.
- A SERP failure puts the reason in the domains cell of that row.
- If pytrends is dead for the whole run, the section header says `Trends unavailable`
  instead of naming it as a source, and every row carries the gap. Run `--no-trends` to
  skip it deliberately, and say so in `{{CAVEATS}}`.
- If Custom Search credentials are missing the script warns and keeps going; every row
  becomes a visible gap. That is a broken run — fix the credentials, don't send it.

Silence is the failure mode to avoid. A row saying the data is missing tells Austin to
check manually; an absent row tells him nothing happened.

## The digest section

Built by `scripts/search_demand.py` and pasted whole into `digest-template.html` at
`#search-demand`, after the competitor sections and before the Chanty note. The markup uses
the digest's own tokens — no new palette.

- One row per term: tier chip, term, trend arrow, top 3 ranking domains.
- **Colour is tier, never direction.** Tier 1 takes the stamp red, Tier 2 the caution gold,
  Tier 3 the neutral rule, Tier 4 neutral and a size smaller. Urgency is what the colour
  is for; the arrow glyph carries direction on its own.
- A domain new to the top 3 this week is underscored.
- Chanty in the top 10 gets a green `✓ #n` badge, so which terms Chanty already owns and
  which are open ground is a glance, not a read.
- Scannable in under a minute. If nothing moved anywhere, omit the whole section.

## Handing gaps to the content idea agent

Every term with a usable SERP writes an entry to `.claude/shared/content-gaps.json`. The
contract is documented in `.claude/shared/README.md`. Categories map to the content idea
agent's own:

| Condition | Category |
|---|---|
| The term is a head-to-head (`… vs …`) | `comparison` |
| Chanty absent from the top 10 and the term is trending up | `trend-jacking` |
| Anything else | `gap` |

Each entry carries the week, term, tier, Chanty's rank or `null`, the top 5 results with
links, and a one-line note — `Chanty is not in the top 10 for "cheaper than slack";
pumble.com, flock.com, zoho.com are.` That is the sentence that becomes a content idea
without anyone having to notice it first.

A rerun for the same week replaces that week's entries rather than duplicating them.

## Where the SERP history lives

The spec asked for SERP results to be stored "in Attio or wherever competitor mentions are
already logged, tagged by term and week". This agent writes no CRM records by design, and
competitor mentions are logged in `state/`, so the history goes to
`state/serp-history.jsonl` — one JSON line per term per week, appended, never rewritten.
It answers the same question ("how did rankings for `slack alternatives` shift over six
months?") without breaking the no-CRM rule. If that history should live in Attio after all,
that is a deliberate change to this agent's boundaries, not a detail.

## Open decisions, and how they ship

1. **Google Chat as a third set** — ships defined but disabled. The taxonomy, the vs-list
   and the tier templates are all in place; `"enabled": true` turns it on. Two reasons to
   wait: the first weeks are when the pytrends rate limit and the SERP quota get their real
   test, and 29 terms is a friendlier first load than 42. Flip it once a run has come back
   clean.
2. **Trends vs. SERP priority** — the SERP half is the backbone and stands alone;
   `--no-trends` produces a complete section with no arrows. Trends is kept because
   direction is what separates "this term is always big" from "this term is moving right
   now", and that is the difference between a standing SEO target and something worth
   writing about this week. If pytrends proves unreliable in practice, switch the weekly to
   `--no-trends` and the section degrades to a ranking table rather than disappearing.
