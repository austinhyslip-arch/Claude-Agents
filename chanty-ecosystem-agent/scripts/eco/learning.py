"""Learning and lookalikes.

The Learning Agent reads what actually happened and proposes changes. This
module does the counting. It never edits policy: it emits recommendations that
a human applies, and it refuses outright to touch the locked fields.
"""

from collections import Counter, defaultdict

from . import policy

LOCKED = {"pricing", "suppression_rules", "compliance_rules", "approved_claims",
          "commercial_terms"}


class LockedFieldError(PermissionError):
    pass


def guard(field):
    if field in LOCKED:
        raise LockedFieldError(
            "the Learning Agent may not modify %r; that is a human decision" % field)
    return True


def _outcome_key(org):
    return org.get("organization_type") or "unknown"


def analyze(organizations, outreach, partners, attribution):
    """Counts, not narratives. The narrative is the agent's job."""
    by_category = defaultdict(lambda: {"orgs": 0, "qualified": 0, "sent": 0,
                                       "responses": 0, "positive": 0, "partners": 0,
                                       "seats": 0, "mrr": 0.0})
    org_index = {o["organization_id"]: o for o in organizations}

    for org in organizations:
        row = by_category[_outcome_key(org)]
        row["orgs"] += 1
        if org.get("state") not in ("DISCOVERED", "RESEARCHING", "DISQUALIFIED", "ARCHIVE"):
            row["qualified"] += 1

    for out in outreach:
        org = org_index.get(out.get("organization_id"))
        if not org:
            continue
        row = by_category[_outcome_key(org)]
        if out.get("status") == "sent":
            row["sent"] += 1
        if out.get("response_classification"):
            row["responses"] += 1
            if out["response_classification"] in ("POSITIVE", "MEETING", "PARTNERSHIP",
                                                  "PROGRAMMING", "REFERRAL"):
                row["positive"] += 1

    for p in partners:
        org = org_index.get(p.get("organization_id"))
        if org:
            by_category[_outcome_key(org)]["partners"] += 1

    for a in attribution:
        org = org_index.get(a.get("organization_id"))
        if not org:
            continue
        row = by_category[_outcome_key(org)]
        row["seats"] += (a.get("direct") or {}).get("seats", 0)
        row["mrr"] += (a.get("direct") or {}).get("mrr", 0)

    offers = Counter()
    offer_wins = Counter()
    for out in outreach:
        if out.get("offer"):
            offers[out["offer"]] += 1
            if out.get("response_classification") in ("POSITIVE", "MEETING", "PARTNERSHIP",
                                                      "PROGRAMMING", "REFERRAL"):
                offer_wins[out["offer"]] += 1

    signals = Counter(o.get("signal_id") is not None for o in outreach)

    return {
        "by_category": {k: dict(v) for k, v in sorted(by_category.items())},
        "offers": {o: {"used": offers[o], "positive": offer_wins[o],
                       "rate": round(offer_wins[o] / offers[o], 3) if offers[o] else None}
                   for o in offers},
        "signal_backed_outreach": signals.get(True, 0),
        "unsignalled_outreach": signals.get(False, 0),
        "seats_total": sum(v["seats"] for v in by_category.values()),
        "mrr_total": round(sum(v["mrr"] for v in by_category.values()), 2),
    }


def archetype(partner, organization, attribution_record=None):
    """The characterization of a win, which is what lookalike search runs on."""
    attribution_record = attribution_record or {}
    direct = attribution_record.get("direct") or {}
    return {
        "organization_type": organization.get("organization_type"),
        "taxonomy_group": organization.get("taxonomy_group"),
        "audience": organization.get("audience_description"),
        "audience_size": organization.get("audience_size"),
        "audience_size_type": organization.get("audience_size_type"),
        "audience_confidence": organization.get("audience_confidence"),
        "vertical": organization.get("industries"),
        "geography": organization.get("geography"),
        "national_or_local": organization.get("national_or_local"),
        "distribution_mechanism": [k for k, v in (organization.get("distribution") or {}).items()
                                   if isinstance(v, dict) and v.get("present")],
        "offer": partner.get("offer"),
        "contact_role": organization.get("contact_status"),
        "signal": organization.get("recent_trigger"),
        "reason_for_yes": partner.get("reason_for_yes"),
        "seats_generated": direct.get("seats", 0),
        "revenue_generated": direct.get("mrr", 0),
        "partner_id": partner.get("partner_id"),
        "source_organization_id": organization.get("organization_id"),
    }


def lookalike_query(archetype_record, limit=50):
    """A search brief, not a search. The Discovery Agent runs it."""
    mechanisms = archetype_record.get("distribution_mechanism") or []
    return {
        "must_match": {
            "organization_type": archetype_record.get("organization_type"),
            "distribution_mechanism_any_of": mechanisms[:3],
        },
        "should_match": {
            "national_or_local": archetype_record.get("national_or_local"),
            "industries_any_of": archetype_record.get("vertical") or [],
            "audience_size_within": _range(archetype_record.get("audience_size")),
        },
        "exclude": {"already_in_store": True, "suppressed": True},
        "limit": limit,
        "why": "resembles %s, which said yes because: %s" % (
            archetype_record.get("partner_id"),
            archetype_record.get("reason_for_yes") or "reason not recorded"),
    }


def _range(size):
    if not size:
        return None
    return [int(size * 0.4), int(size * 2.5)]


def recommendations(analysis, min_sample=8):
    """Only speak where there is enough data to speak. Silence beats noise."""
    out = []
    for category, row in analysis["by_category"].items():
        if row["sent"] < min_sample:
            out.append({"field": "targeting", "category": category,
                        "recommendation": "keep testing, %d sends is not enough to judge"
                                          % row["sent"], "confidence": "low"})
            continue
        rate = row["positive"] / row["sent"] if row["sent"] else 0
        if rate >= 0.15:
            out.append({"field": "targeting", "category": category,
                        "recommendation": "expand discovery, %.0f%% positive reply rate"
                                          % (rate * 100), "confidence": "medium"})
        elif rate <= 0.02:
            out.append({"field": "targeting", "category": category,
                        "recommendation": "pause discovery, %.0f%% positive reply rate"
                                          % (rate * 100), "confidence": "medium"})
    for offer, row in analysis["offers"].items():
        if row["used"] >= min_sample and row["rate"] is not None:
            out.append({"field": "offer_prioritization", "offer": offer,
                        "recommendation": "%s converts at %.0f%% over %d uses"
                                          % (offer, row["rate"] * 100, row["used"]),
                        "confidence": "medium"})
    for rec in out:
        guard(rec["field"])
    return out
