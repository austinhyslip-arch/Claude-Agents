"""Attribution and the partner value model.

Direct and assisted are kept apart everywhere. Mixing them is how a channel
program ends up claiming credit it cannot defend.
"""

from . import ids, policy, store

EMPTY = {
    "reach": 0, "registrations": 0, "attendees": 0, "visits": 0, "signups": 0,
    "activated_teams": 0, "paid_accounts": 0, "seats": 0, "mrr": 0, "arr": 0,
}


def next_sequence(org_type, root=None, records=None):
    records = records if records is not None else store.all("attribution", root)
    prefix = "CHANTY-%s-" % ids.slugify(org_type, 12)
    used = [r["attribution_id"] for r in records if r["attribution_id"].startswith(prefix)]
    return len(used) + 1


def create(organization, root=None, records=None, tracking_base="https://www.chanty.com/partners"):
    org_type = organization.get("organization_type") or "PARTNER"
    seq = next_sequence(org_type, root=root, records=records)
    aid = ids.attribution_id(org_type, organization["organization_name"], seq)
    record = {
        "attribution_id": aid,
        "organization_id": organization["organization_id"],
        "partner_id": None,
        "tracking_url": "%s/%s" % (tracking_base.rstrip("/"), aid.lower()),
        "direct": dict(EMPTY),
        "assisted": dict(EMPTY),
        "distribution_events": [],
        "created_at": None,
        "updated_at": None,
    }
    return record


def add_outcome(record, kind, **metrics):
    """kind is 'direct' or 'assisted'. Unknown metric names are rejected."""
    if kind not in ("direct", "assisted"):
        raise ValueError("kind must be direct or assisted")
    bucket = record.setdefault(kind, dict(EMPTY))
    for key, value in metrics.items():
        if key not in EMPTY:
            raise ValueError("unknown attribution metric %r" % key)
        bucket[key] = bucket.get(key, 0) + value
    return record


def expected_paid_seats(audience, overrides=None, policy_path=None):
    """Audience x ICP fit x reach x trial x activation x paid conversion x seats.

    Returns the number and the inputs that produced it, flagged by whether each
    input is an assumption or an observation. A forecast whose provenance is not
    visible is a guess with a decimal point.
    """
    defaults = policy.get("partner_value_model_defaults", {}, path=policy_path)
    params = {k: v for k, v in defaults.items() if not k.startswith("_")}
    params.update(overrides or {})

    seats = (
        float(audience or 0)
        * float(params.get("icp_fit", 0))
        * float(params.get("reach_rate", 0))
        * float(params.get("trial_rate", 0))
        * float(params.get("activation_rate", 0))
        * float(params.get("paid_conversion", 0))
        * float(params.get("average_seats", 0))
    )
    seats = round(seats, 1)
    return {
        "expected_paid_seats": seats,
        "expected_mrr": round(seats * policy.price_per_seat(path=policy_path), 2),
        "inputs": params,
        "basis": params.get("source", "assumption"),
        "audience": audience,
    }


def observed_rates(attribution_records):
    """Replace assumptions with observed rates once there is data to observe."""
    totals = {k: 0 for k in EMPTY}
    for rec in attribution_records:
        for k in EMPTY:
            totals[k] += (rec.get("direct") or {}).get(k, 0)

    def ratio(num, den):
        return round(totals[num] / totals[den], 4) if totals.get(den) else None

    return {
        "observations_count": len(attribution_records),
        "trial_rate": ratio("signups", "reach"),
        "activation_rate": ratio("activated_teams", "signups"),
        "paid_conversion": ratio("paid_accounts", "activated_teams"),
        "average_seats": ratio("seats", "paid_accounts"),
        "totals": totals,
        "source": "observed" if attribution_records else "assumption",
    }
