"""Expand the search-term taxonomy in references/search-terms.json into concrete terms.

The taxonomy is data, not code: adding Google Chat as a third full keyword set is a
matter of flipping `enabled` in the JSON. Nothing here touches the network.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "references" / "search-terms.json"


@dataclass(frozen=True)
class Term:
    """One concrete search term, with the metadata the digest row needs."""

    query: str
    tier: int
    tier_name: str
    set_id: str
    set_label: str

    @property
    def key(self) -> str:
        """Stable cache key. The query text is the identity — tiers can be re-cut."""
        return self.query


def load_config(path: Path | str | None = None) -> dict:
    with open(path or CONFIG_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _render(pattern: str, *, target: str, short: str, vs: str, year: int) -> str:
    return (
        pattern.replace("{target}", target)
        .replace("{short}", short)
        .replace("{vs}", vs)
        .replace("{year}", str(year))
    )


def expand(config: dict, year: int | None = None) -> list[Term]:
    """Return every term the taxonomy currently produces, de-duplicated, tier order first.

    A term that two sets would both produce (a `slack vs teams` / `teams vs slack` style
    collision, or any global term) is kept once, under the first tier that claims it.
    """
    year = year or _dt.date.today().year
    sets = [s for s in config.get("sets", []) if s.get("enabled", False)]
    terms: list[Term] = []
    seen: set[str] = set()

    for tier_key in sorted(config.get("tiers", {}), key=int):
        tier = config["tiers"][tier_key]
        tier_no = int(tier_key)
        for template in tier.get("templates", []):
            scope = template.get("scope", "set")
            pattern = template["pattern"]

            if scope == "global":
                query = _render(pattern, target="", short="", vs="", year=year).strip()
                candidates = [(query, "_global", "All")]
            else:
                candidates = []
                for s in sets:
                    vs_values = s.get("vs", []) if "{vs}" in pattern else [""]
                    for vs_value in vs_values:
                        query = _render(
                            pattern,
                            target=s["target"],
                            short=s["short"],
                            vs=vs_value,
                            year=year,
                        ).strip()
                        candidates.append((query, s["id"], s["label"]))

            for query, set_id, set_label in candidates:
                norm = " ".join(query.lower().split())
                if not norm or norm in seen:
                    continue
                seen.add(norm)
                terms.append(
                    Term(
                        query=norm,
                        tier=tier_no,
                        tier_name=tier.get("name", f"Tier {tier_no}"),
                        set_id=set_id,
                        set_label=set_label,
                    )
                )
    return terms


if __name__ == "__main__":  # `python3 search_terms.py` prints the live list
    cfg = load_config()
    for t in expand(cfg):
        print(f"T{t.tier}  {t.set_label:<16} {t.query}")
