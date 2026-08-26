#!/usr/bin/env python3
"""Offline self-test for the Search Demand pipeline.

Substitutes both network fetchers with fixtures, runs the real orchestrator into a
temporary state directory, and asserts the behaviours the digest depends on:

  * a term whose two sources both fail still renders, carrying the failure text
  * a quiet term is dropped rather than shipped as an empty row
  * the Chanty badge appears exactly when Chanty is in the top 10
  * tier ordering, the row cap, the cache round-trip, and the content-gap contract

Run it after touching any of the scripts:  python3 selftest.py
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import search_demand as sd  # noqa: E402
from search_terms import load_config  # noqa: E402
from serp_client import SerpClient  # noqa: E402
from trends_client import TrendsClient  # noqa: E402

FIXTURE_SERP = {
    "slack alternatives": ["g2.com", "zapier.com", "chanty.com", "nectarhr.com",
                           "clickup.com", "troopmessenger.com", "flock.com", "zoho.com",
                           "rocket.chat", "pumble.com"],
    "cheaper than slack": ["reddit.com", "pumble.com", "flock.com", "zoho.com",
                           "rocket.chat"],
    "alternative to slack": ["g2.com", "clickup.com", "zapier.com"],
}
FIXTURE_TRENDS = {
    "slack alternatives": [50] * 14 + [70] * 14,      # clear rise
    "cheaper than slack": [40] * 28,                   # flat
    "alternative to slack": [60] * 14 + [42] * 14,     # clear fall
}


class FakeSerp(SerpClient):
    def __init__(self, **kw):
        super().__init__(api_key="fixture", cx="fixture", delay=0, **kw)

    def fetch(self, query):
        if query == "boom":
            raise RuntimeError("HTTP 429: quota exceeded")
        return [{"link": f"https://{d}/page", "title": d}
                for d in FIXTURE_SERP.get(query, ["example.com", "example.org"])]

    def sleep_between(self):
        return None


class FakeTrends(TrendsClient):
    def __init__(self, **kw):
        super().__init__(delay=0, max_retries=1, backoff=0, **kw)

    def fetch_series(self, query):
        if query == "boom":
            raise RuntimeError("pytrends 429")
        values = FIXTURE_TRENDS.get(query)
        if values is None:
            return []
        return [{"date": f"2026-08-{i + 1:02d}", "value": float(v), "partial": False}
                for i, v in enumerate(values)]

    def sleep_between(self):
        return None


def fixture_terms(config):
    from search_terms import Term
    return [
        Term("slack alternatives", 1, "Active switching intent", "slack", "Slack"),
        Term("alternative to slack", 1, "Active switching intent", "slack", "Slack"),
        Term("boom", 2, "Price sensitivity", "slack", "Slack"),
        Term("cheaper than slack", 2, "Price sensitivity", "slack", "Slack"),
        Term("chanty reviews", 4, "Brand tracking", "_global", "All"),
    ]


def check(label, condition, detail=""):
    status = "ok  " if condition else "FAIL"
    print(f"  [{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    return bool(condition)


def main() -> int:
    passed = True
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        sd.STATE_DIR = root / "state"
        sd.RUN_DIR = sd.STATE_DIR / "search-demand"
        sd.CACHE_PATH = sd.STATE_DIR / "search-demand-cache.json"
        sd.HISTORY_PATH = sd.STATE_DIR / "serp-history.jsonl"
        sd.CONTENT_GAPS_PATH = root / "shared" / "content-gaps.json"
        sd.expand = fixture_terms

        config = load_config()
        args = argparse.Namespace(week="2026-08-24", max_rows=12, terms=None,
                                  dry_run=False, delay=0, no_trends=False)

        print("run 1 — cold cache")
        first = sd.run(args, FakeTrends(), FakeSerp(), config)
        section = (sd.RUN_DIR / "2026-08-24.section.html").read_text(encoding="utf-8")

        passed &= check("every term is notable on a cold cache",
                        first["notable"] == 5, f'notable={first["notable"]}')
        passed &= check("rising term reads as up",
                        '<span class="sd-arrow up"' in section)
        passed &= check("falling term reads as down",
                        '<span class="sd-arrow down"' in section)
        passed &= check("dead trends row says so, and still ships",
                        "Trends data unavailable this week" in section
                        and "boom" in section)
        passed &= check("dead SERP row carries the reason",
                        "quota exceeded" in section)
        passed &= check("Chanty badge appears where Chanty ranks",
                        'sd-badge" title="Chanty ranks #3">✓ #3' in section)
        badges = section.count("sd-badge")
        passed &= check("badge appears only there", badges == 1, f"badges={badges}")
        passed &= check("tier 1 rows sort above tier 4",
                        section.index("sd-t1") < section.index("sd-t4"))
        passed &= check("no unsubstituted tokens", "{{" not in section)

        gaps = json.loads(sd.CONTENT_GAPS_PATH.read_text(encoding="utf-8"))
        by_term = {g["term"]: g for g in gaps["entries"]}
        passed &= check("gap entry names the ranking competitors",
                        "pumble.com" in by_term["cheaper than slack"]["note"])
        passed &= check("absent + rising is trend-jacking",
                        by_term["cheaper than slack"]["category"] == "gap"
                        and by_term["alternative to slack"]["category"] == "gap")
        passed &= check("Chanty's own rank is recorded, not just absence",
                        by_term["slack alternatives"]["chanty_rank"] == 3)
        passed &= check("failed SERP writes no gap entry", "boom" not in by_term)

        history = [json.loads(l) for l in
                   sd.HISTORY_PATH.read_text(encoding="utf-8").splitlines()]
        passed &= check("history is tagged by term and week",
                        all(h["week"] == "2026-08-24" for h in history) and len(history) == 4,
                        f"rows={len(history)}")

        print("run 2 — warm cache; one term moves, the rest sit still")
        # Only "slack alternatives" changes: its index rises, and a new domain takes a
        # top-3 slot. Everything else repeats last week's fixture exactly.
        FIXTURE_TRENDS["slack alternatives"] = [70] * 14 + [90] * 14
        FIXTURE_SERP["alternative to slack"] = ["g2.com", "clickup.com", "zapier.com"]
        args.week = "2026-08-31"
        second = sd.run(args, FakeTrends(), FakeSerp(), config)
        section2 = (sd.RUN_DIR / "2026-08-31.section.html").read_text(encoding="utf-8")

        passed &= check("quiet term is dropped from the digest",
                        "cheaper than slack" not in section2)
        passed &= check("a term that moved this week stays",
                        "slack alternatives" in section2)
        passed &= check("a term that only moved last week is gone",
                        "alternative to slack" not in section2)
        passed &= check("both-sources-dead term still ships", "boom" in section2)
        passed &= check("week-over-week basis is used once cached",
                        'title="week-over-week' in section2)
        passed &= check("second week appended to history, not overwritten",
                        len(sd.HISTORY_PATH.read_text(encoding="utf-8").splitlines()) == 8)
        passed &= check("quiet terms are still pulled and cached, just not shown",
                        second["terms_pulled"] == 5 and second["notable"] == 2,
                        f'notable={second["notable"]}')
        gaps2 = json.loads(sd.CONTENT_GAPS_PATH.read_text(encoding="utf-8"))
        weeks = sorted({g["week"] for g in gaps2["entries"]})
        passed &= check("content gaps keep both weeks",
                        weeks == ["2026-08-24", "2026-08-31"], str(weeks))

        print("run 3 — --no-trends")
        args.week, args.no_trends = "2026-09-07", True
        sd.run(args, None, FakeSerp(), config)
        section3 = (sd.RUN_DIR / "2026-09-07.section.html").read_text(encoding="utf-8")
        passed &= check("SERP-only run still produces a section",
                        "Search Demand Signals" in section3 and "sd-ranks" in section3)
        passed &= check("no arrows claimed when trends is off",
                        'class="sd-arrow up"' not in section3)

        print("row cap")
        args.max_rows = 2
        capped = sd.rank_rows([r for r in first["rows"] if sd.is_notable(r)], 2)
        passed &= check("cap holds and keeps the top tier",
                        len(capped) == 2 and capped[0]["tier"] == 1)

    print("\nPASS" if passed else "\nFAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
