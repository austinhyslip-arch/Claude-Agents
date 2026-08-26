#!/usr/bin/env python3
"""Search Demand Signals — the weekly switching-intent pull for the Chanty digest.

Runs the search-term taxonomy against two sources: Google Trends (interest over time, via
pytrends) and the Google Custom Search API (who ranks right now). Produces four things:

  1. an HTML fragment for the "Search Demand Signals" section of the Monday digest
  2. a full JSON snapshot of the run, notable rows and quiet ones alike
  3. an append to the SERP history, so rankings can be diffed over months, not just weeks
  4. content-gap entries in the shared file the content idea agent reads

Nothing here aborts the digest. A dead source degrades to a visible gap in a row.

Usage
  python3 search_demand.py                      # full weekly run
  python3 search_demand.py --no-trends          # SERP-only, no arrows
  python3 search_demand.py --terms 5 --dry-run  # smoke test, writes nothing
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import sys
from pathlib import Path

from search_terms import Term, expand, load_config
from serp_client import SerpClient, SerpResult
from trends_client import TrendResult, TrendsClient

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parents[2]                       # .claude/skills/<skill> -> repo root
STATE_DIR = SKILL_DIR / "state"
RUN_DIR = STATE_DIR / "search-demand"
CACHE_PATH = STATE_DIR / "search-demand-cache.json"
HISTORY_PATH = STATE_DIR / "serp-history.jsonl"
CONTENT_GAPS_PATH = REPO_ROOT / ".claude" / "shared" / "content-gaps.json"

ARROW_GLYPH = {"up": "▲", "down": "▼", "flat": "–", "unavailable": ""}
DEFAULT_MAX_ROWS = 12


# --------------------------------------------------------------------------- rows


def build_row(term: Term, trend: TrendResult, serp: SerpResult, chanty_domains: list[str],
              cached: dict) -> dict:
    """Merge one term's two pulls into the row the digest and the JSON both use."""
    prev_top3 = cached.get("top3", [])
    prev_chanty_rank = cached.get("chanty_rank")
    chanty_rank = serp.rank_of(chanty_domains) if serp.ok else None
    top3 = serp.top(3) if serp.ok else []

    entered = [d for d in top3 if d not in prev_top3]
    left = [d for d in prev_top3 if d not in top3]

    return {
        "term": term.query,
        "tier": term.tier,
        "tier_name": term.tier_name,
        "set": term.set_id,
        "set_label": term.set_label,
        "trend": {
            "ok": trend.ok,
            "arrow": trend.arrow,
            "delta_pct": trend.delta_pct,
            "basis": trend.basis,
            "latest": trend.latest,
            "reason": trend.reason,
        },
        "serp": {
            "ok": serp.ok,
            "reason": serp.reason,
            "top3": top3,
            "top10": serp.results,
            "chanty_rank": chanty_rank,
        },
        "movement": {
            "first_seen": not cached,
            "entered_top3": entered if prev_top3 else [],
            "left_top3": left if prev_top3 else [],
            "chanty_rank_prev": prev_chanty_rank,
            "chanty_entered": chanty_rank is not None and prev_chanty_rank is None,
            "chanty_left": chanty_rank is None and prev_chanty_rank is not None,
        },
    }


def is_notable(row: dict) -> bool:
    """Quiet terms are dropped from the digest, not shipped as empty boxes.

    A row earns its line when the trend moved, the top 3 changed, Chanty's position
    changed, or we have never recorded the term before (a baseline is worth seeing once).
    A row whose sources both failed is notable too — a silent failure is the thing this
    section is least allowed to do.
    """
    if row["movement"]["first_seen"]:
        return True
    if row["trend"]["arrow"] in ("up", "down"):
        return True
    if row["movement"]["entered_top3"] or row["movement"]["left_top3"]:
        return True
    if row["movement"]["chanty_entered"] or row["movement"]["chanty_left"]:
        return True
    if not row["trend"]["ok"] and not row["serp"]["ok"]:
        return True
    return False


def rank_rows(rows: list[dict], max_rows: int) -> list[dict]:
    """Tier first — tier is what says how urgent this is — then size of the move."""

    def sort_key(row: dict):
        delta = abs(row["trend"]["delta_pct"] or 0)
        chanty_move = row["movement"]["chanty_entered"] or row["movement"]["chanty_left"]
        return (row["tier"], not chanty_move, -delta, row["term"])

    return sorted(rows, key=sort_key)[:max_rows]


# --------------------------------------------------------------------------- outputs


def render_section(rows: list[dict], total_terms: int, notable_count: int,
                   sources_note: str) -> str:
    """The HTML fragment. Classes and colors come from digest-template.html."""
    if not rows:
        return ""

    parts = [
        '  <!-- ============ SEARCH DEMAND SIGNALS ============ -->',
        '  <section id="search-demand">',
        '    <div class="section-head">',
        '      <h2>Search Demand Signals</h2>',
        f'      <span class="count">{notable_count} of {total_terms} terms moved · '
        f'{html.escape(sources_note)}</span>',
        '    </div>',
        '    <ol class="sd-rows">',
    ]

    for row in rows:
        tier = row["tier"]
        classes = f"sd-row sd-t{tier}"
        term = html.escape(row["term"])

        badge = ""
        rank = row["serp"]["chanty_rank"]
        if rank is not None:
            badge = f' <span class="sd-badge" title="Chanty ranks #{rank}">✓ #{rank}</span>'

        trend = row["trend"]
        if trend["ok"] and trend["arrow"] != "unavailable":
            delta = trend["delta_pct"]
            label = f'{delta:+.0f}%' if delta is not None else ""
            title = f'{trend["basis"]} · index {trend["latest"]:g}' if trend["latest"] else ""
            arrow_cell = (
                f'<span class="sd-arrow {trend["arrow"]}" title="{html.escape(title)}">'
                f'{ARROW_GLYPH[trend["arrow"]]}<i>{label}</i></span>'
            )
        else:
            arrow_cell = '<span class="sd-arrow na">Trends data unavailable this week</span>'

        if row["serp"]["ok"] and row["serp"]["top3"]:
            domains = []
            for domain in row["serp"]["top3"]:
                mark = " sd-new" if domain in row["movement"]["entered_top3"] else ""
                domains.append(f'<b class="sd-dom{mark}">{html.escape(domain)}</b>')
            ranks_cell = f'<span class="sd-ranks">{" · ".join(domains)}</span>'
        else:
            reason = row["serp"]["reason"] or "no SERP data"
            ranks_cell = f'<span class="sd-ranks sd-na">{html.escape(reason)}</span>'

        parts += [
            f'      <li class="{classes}">',
            f'        <span class="sd-tier">T{tier}</span>',
            f'        <span class="sd-term">{term}{badge}</span>',
            f'        {arrow_cell}',
            f'        {ranks_cell}',
            '      </li>',
        ]

    parts += ['    </ol>', '  </section>', '']
    return "\n".join(parts)


def content_gap_entries(rows: list[dict], week: str) -> list[dict]:
    """Gap findings for the content idea agent. Contract: .claude/shared/README.md."""
    entries = []
    for row in rows:
        if not row["serp"]["ok"] or not row["serp"]["top3"]:
            continue
        rank = row["serp"]["chanty_rank"]
        absent = rank is None
        if " vs " in row["term"]:
            category = "comparison"
        elif absent and row["trend"]["arrow"] == "up":
            category = "trend-jacking"
        else:
            category = "gap"

        top3 = row["serp"]["top3"]
        if absent:
            note = (f'Chanty is not in the top 10 for "{row["term"]}"; '
                    f'{", ".join(top3)} are.')
        else:
            note = f'Chanty ranks #{rank} for "{row["term"]}"; {", ".join(top3)} rank above.'

        entries.append({
            "week": week,
            "term": row["term"],
            "tier": row["tier"],
            "set": row["set"],
            "category": category,
            "chanty_rank": rank,
            "trend": row["trend"]["arrow"],
            "top_domains": row["serp"]["top10"][:5],
            "note": note,
        })
    return entries


def write_content_gaps(entries: list[dict], path: Path) -> int:
    """Append this week's entries, replacing any earlier write for the same week."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"source": "chanty-competitive-intel/search-demand", "entries": []}
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8")) or payload
        except json.JSONDecodeError:
            pass
    weeks = {e["week"] for e in entries}
    kept = [e for e in payload.get("entries", []) if e.get("week") not in weeks]
    payload["entries"] = kept + entries
    payload["updated"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return len(entries)


def append_history(rows: list[dict], week: str, path: Path) -> None:
    """One JSON line per term per week — the long view on how rankings shift."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for row in rows:
            if not row["serp"]["ok"]:
                continue
            fh.write(json.dumps({
                "week": week,
                "term": row["term"],
                "tier": row["tier"],
                "set": row["set"],
                "chanty_rank": row["serp"]["chanty_rank"],
                "results": [
                    {"rank": r["rank"], "domain": r["domain"], "link": r["link"]}
                    for r in row["serp"]["top10"]
                ],
            }, ensure_ascii=False) + "\n")


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("terms", {})
    except (json.JSONDecodeError, AttributeError):
        return {}


def save_cache(rows: list[dict], week: str, path: Path, previous: dict) -> None:
    """Carry a term's last good values forward when this week's pull failed."""
    terms = dict(previous)
    for row in rows:
        entry = dict(terms.get(row["term"], {}))
        entry["week"] = week
        if row["trend"]["ok"]:
            entry["latest"] = row["trend"]["latest"]
            entry["arrow"] = row["trend"]["arrow"]
        if row["serp"]["ok"]:
            entry["top3"] = row["serp"]["top3"]
            entry["chanty_rank"] = row["serp"]["chanty_rank"]
        terms[row["term"]] = entry
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "week": week,
        "terms": terms,
    }, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- run


def run(args, trends: TrendsClient | None, serp: SerpClient, config: dict) -> dict:
    week = args.week or dt.date.today().isoformat()
    terms = expand(config)
    if args.terms:
        terms = terms[: args.terms]
    chanty_domains = config.get("chanty_domains", ["chanty.com"])
    cache = load_cache(CACHE_PATH)

    rows: list[dict] = []
    trend_failures = 0
    serp_failures = 0

    for index, term in enumerate(terms):
        cached = cache.get(term.query, {})
        if trends is None:
            trend = TrendResult(query=term.query, reason="trends disabled for this run")
        else:
            trend = trends.interest(term.query, previous_latest=cached.get("latest"))
            if not trend.ok:
                trend_failures += 1
                print(f"  trends failed: {term.query} — {trend.reason}", file=sys.stderr)
            if index < len(terms) - 1:
                trends.sleep_between()

        result = serp.search(term.query)
        if not result.ok:
            serp_failures += 1
            print(f"  serp failed: {term.query} — {result.reason}", file=sys.stderr)
        if index < len(terms) - 1:
            serp.sleep_between()

        rows.append(build_row(term, trend, result, chanty_domains, cached))

    notable = [r for r in rows if is_notable(r)]
    shown = rank_rows(notable, args.max_rows)

    sources = []
    if trends is not None:
        sources.append("Google Trends" if trend_failures < len(terms) else "Trends unavailable")
    sources.append("Custom Search" if serp_failures < len(terms) else "SERP unavailable")

    section = render_section(shown, len(terms), len(notable), " + ".join(sources))
    summary = {
        "week": week,
        "terms_pulled": len(terms),
        "notable": len(notable),
        "shown": len(shown),
        "trend_failures": trend_failures,
        "serp_failures": serp_failures,
        "rows": rows,
        "shown_terms": [r["term"] for r in shown],
    }

    if args.dry_run:
        print(section or "(no notable rows — omit the section from the digest)")
        print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=2),
              file=sys.stderr)
        return summary

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (RUN_DIR / f"{week}.json").write_text(json.dumps(summary, indent=2) + "\n",
                                          encoding="utf-8")
    section_path = RUN_DIR / f"{week}.section.html"
    section_path.write_text(section, encoding="utf-8")
    append_history(rows, week, HISTORY_PATH)
    gaps = write_content_gaps(content_gap_entries(rows, week), CONTENT_GAPS_PATH)
    save_cache(rows, week, CACHE_PATH, cache)

    print(f"{len(terms)} terms pulled · {len(notable)} notable · {len(shown)} in the digest")
    print(f"trends failures {trend_failures} · serp failures {serp_failures} · "
          f"{gaps} content-gap entries")
    print(f"section  -> {section_path}")
    print(f"snapshot -> {RUN_DIR / (week + '.json')}")
    return summary


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--week", help="ISO date to file this run under (default: today)")
    parser.add_argument("--max-rows", type=int, default=DEFAULT_MAX_ROWS,
                        help="cap on digest rows so the section stays one screen")
    parser.add_argument("--terms", type=int, help="only pull the first N terms (smoke test)")
    parser.add_argument("--no-trends", action="store_true",
                        help="skip pytrends entirely and ship the SERP half only")
    parser.add_argument("--delay", type=float, default=None,
                        help="seconds between pytrends calls (default 4)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the section and the summary, write nothing")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    config = load_config()
    trends = None
    if not args.no_trends:
        trends = TrendsClient(
            geo=config.get("geo", "US"),
            timeframe=config.get("timeframe", "today 3-m"),
            **({"delay": args.delay} if args.delay is not None else {}),
        )
    serp = SerpClient(depth=config.get("serp_depth", 10), geo=config.get("geo", "US"))
    if not serp.configured:
        print("warning: Custom Search credentials are not set — every SERP row will be "
              "a visible gap. Set GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX.", file=sys.stderr)
    run(args, trends, serp, config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
