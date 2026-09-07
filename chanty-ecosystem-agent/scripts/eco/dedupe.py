"""Deduplication.

Checks in the order the spec calls for: exact domain, normalized name, LinkedIn
URL, then parent + chapter + location. A national body and its local chapter are
different organizations and must not be merged, so the chapter check runs on the
combination, never on the parent alone.
"""

import re
from urllib.parse import urlparse

from . import ids, store

_NOISE = {
    "the", "inc", "inc.", "llc", "ltd", "co", "corp", "corporation",
    "association", "assn", "org", "organization", "of", "and", "&",
}


def normalize_domain(value):
    if not value:
        return None
    value = value.strip().lower()
    if "//" not in value:
        value = "https://" + value
    host = urlparse(value).netloc or ""
    host = host.split("@")[-1].split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return host or None


def normalize_name(value):
    if not value:
        return ""
    text = re.sub(r"[^a-z0-9 ]+", " ", value.lower())
    words = [w for w in text.split() if w and w not in _NOISE]
    return " ".join(words)


def normalize_linkedin(value):
    if not value:
        return None
    value = value.strip().lower().rstrip("/")
    parsed = urlparse(value if "//" in value else "https://" + value)
    path = parsed.path.rstrip("/")
    return path or None


def identity_seed(candidate):
    """The seed that produces the organization_id.

    Domain first because it is the strongest signal. Chapters of the same parent
    that share a domain are separated by their chapter name, which is why the
    chapter is part of the seed.
    """
    domain = normalize_domain(candidate.get("domain") or candidate.get("website"))
    chapter = normalize_name(candidate.get("chapter"))
    if domain:
        return "|".join(["domain", domain, chapter])
    return "|".join([
        "name",
        normalize_name(candidate.get("organization_name")),
        normalize_name(candidate.get("city")),
        normalize_name(candidate.get("state_region")),
        chapter,
    ])


def proposed_id(candidate):
    return ids.make_id("organizations", identity_seed(candidate))


def find_duplicate(candidate, existing=None, root=None):
    """Return (record, reason) for the first match, or (None, None).

    Two organizations that differ in chapter are never treated as duplicates,
    whatever else they share.
    """
    existing = existing if existing is not None else store.all("organizations", root)
    cand_domain = normalize_domain(candidate.get("domain") or candidate.get("website"))
    cand_name = normalize_name(candidate.get("organization_name"))
    cand_li = normalize_linkedin(candidate.get("linkedin"))
    cand_chapter = normalize_name(candidate.get("chapter"))
    cand_parent = normalize_name(candidate.get("parent_organization"))
    cand_city = normalize_name(candidate.get("city"))

    for rec in existing:
        rec_chapter = normalize_name(rec.get("chapter"))
        different_chapter = bool(cand_chapter or rec_chapter) and cand_chapter != rec_chapter
        if different_chapter:
            continue

        rec_domain = normalize_domain(rec.get("domain") or rec.get("website"))
        if cand_domain and rec_domain and cand_domain == rec_domain:
            return rec, "exact_domain"
        if cand_name and cand_name == normalize_name(rec.get("organization_name")):
            return rec, "normalized_name"
        rec_li = normalize_linkedin(rec.get("linkedin"))
        if cand_li and rec_li and cand_li == rec_li:
            return rec, "linkedin_url"
        if (cand_parent and cand_parent == normalize_name(rec.get("parent_organization"))
                and cand_city and cand_city == normalize_name(rec.get("city"))):
            return rec, "parent_and_location"
    return None, None
