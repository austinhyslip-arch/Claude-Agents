"""Record IDs and partner attribution IDs."""

import hashlib
import re

PREFIXES = {
    "organizations": "ORG",
    "contacts": "CON",
    "opportunities": "OPP",
    "signals": "SIG",
    "partners": "PTR",
    "outreach": "OUT",
    "suppression": "SUP",
    "executions": "EXE",
}

_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _b36(digest, length=8):
    n = int.from_bytes(digest[:8], "big")
    out = ""
    while n and len(out) < length:
        n, rem = divmod(n, 36)
        out += _ALPHABET[rem]
    return out.rjust(length, "0")[:length]


def make_id(collection, seed):
    """Deterministic from the seed, so the same organization gets the same ID.

    That is what makes dedupe idempotent across runs.
    """
    prefix = PREFIXES[collection]
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return "%s-%s" % (prefix, _b36(digest))


def slugify(text, maxlen=24):
    slug = re.sub(r"[^A-Za-z0-9]+", "-", (text or "")).strip("-").upper()
    return slug[:maxlen].strip("-")


def attribution_id(org_type, org_name, sequence):
    """CHANTY-CHAMBER-KC-001 style. Stable, readable, greppable in a URL."""
    return "CHANTY-%s-%s-%03d" % (slugify(org_type, 12), slugify(org_name, 18), sequence)
