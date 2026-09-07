"""Policy access. Read-only, on purpose.

Nothing in this package writes to config/policy.json. If code ever needs to,
that is a bug: policy changes are a human action.
"""

import json
import os

from . import paths

_cache = {}


def load(path=None):
    path = path or paths.POLICY_FILE
    key = os.path.abspath(path)
    mtime = os.path.getmtime(key)
    cached = _cache.get(key)
    if cached and cached[0] == mtime:
        return cached[1]
    with open(key) as fh:
        data = json.load(fh)
    _cache[key] = (mtime, data)
    return data


def get(dotted, default=None, path=None):
    node = load(path)
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def price_per_seat(path=None):
    return get("chanty_pricing.price_per_seat_usd", path=path)


def max_touches(path=None):
    return get("max_touches", 4, path=path)


def autonomy_level(path=None):
    return get("autonomy.current_level", 0, path=path)


def enrichment_allowed(path=None):
    return bool(get("contact_data_policy.enrichment_allowed", False, path=path))


def blocked_tool(tool_name, path=None):
    """True when a tool name is barred by the contact data policy.

    Checked by name so a newly connected enrichment MCP server does not quietly
    become permitted just because nobody updated a list of vendors.
    """
    cdp = get("contact_data_policy", {}, path=path)
    for prefix in cdp.get("blocked_tool_prefixes", []):
        if tool_name.startswith(prefix):
            return True
    return tool_name in cdp.get("blocked_tool_names", [])


def band_for_score(score, path=None):
    for band in get("scoring.bands", [], path=path):
        if band["min"] <= score <= band["max"]:
            return band["name"]
    return "ARCHIVE"


def signal_decay_band(age_days, path=None):
    for band in get("signal_decay", [], path=path):
        lo, hi = band["min_days"], band["max_days"]
        if age_days >= lo and (hi is None or age_days <= hi):
            return band["band"]
    return "historical"
