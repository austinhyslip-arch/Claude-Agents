"""Weekly and monthly reporting.

Operational counts are reported because they are useful for debugging the
pipeline. They are labelled operational so nobody mistakes them for the point.
The business metric, stated last and stated plainly, is paid seats.
"""

import datetime

from . import learning, policy


def _since(days):
    return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)


def _created_after(records, cutoff, field="created_at"):
    out = []
    for r in records:
        stamp = r.get(field)
        if not stamp:
            continue
        try:
            when = datetime.datetime.fromisoformat(stamp)
        except ValueError:
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        if when >= cutoff:
            out.append(r)
    return out


def weekly(organizations, outreach, signals, partners, attribution, days=7):
    cutoff = _since(days)
    new_orgs = _created_after(organizations, cutoff)
    bands = {}
    for org in organizations:
        bands.setdefault(org.get("priority_band") or "UNSCORED", []).append(org)

    sent = [o for o in outreach if o.get("status") == "sent"]
    responses = [o for o in outreach if o.get("response_classification")]
    positive = [o for o in responses if o["response_classification"] in
                ("POSITIVE", "MEETING", "PARTNERSHIP", "PROGRAMMING", "REFERRAL")]
    meetings = [o for o in responses if o["response_classification"] == "MEETING"]

    direct = {"trials": 0, "paid_accounts": 0, "seats": 0, "mrr": 0.0}
    for a in attribution:
        d = a.get("direct") or {}
        direct["trials"] += d.get("signups", 0)
        direct["paid_accounts"] += d.get("paid_accounts", 0)
        direct["seats"] += d.get("seats", 0)
        direct["mrr"] += d.get("mrr", 0)

    analysis = learning.analyze(organizations, outreach, partners, attribution)
    best = _best(analysis)

    return {
        "period_days": days,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "operational": {
            "new_organizations": len(new_orgs),
            "qualified": len([o for o in organizations if o.get("state") not in
                              ("DISCOVERED", "RESEARCHING", "DISQUALIFIED")]),
            "tier_1": len(bands.get("TIER_1", [])),
            "tier_2": len(bands.get("TIER_2", [])),
            "strategic": len(bands.get("STRATEGIC", [])),
            "nurture": len(bands.get("NURTURE", [])),
            "outreach_sent": len(sent),
            "responses": len(responses),
            "positive_responses": len(positive),
            "meetings": len(meetings),
            "new_signals": len(_created_after(signals, cutoff)),
            "drafts_awaiting_review": len([o for o in outreach if o.get("status")
                                           in ("draft", "human_review")]),
            "email_not_public": len([o for o in organizations
                                     if o.get("state") == "EMAIL_NOT_PUBLIC"]),
            "enrichment_used": 0,
        },
        "partnerships": {
            "total": len(partners),
            "live": len([p for p in partners if p.get("partnership_stage") == "live"]),
            "activated": len([p for p in partners if p.get("activated")]),
            "distribution_occurred": len([p for p in partners
                                          if p.get("distribution_occurred")]),
        },
        "business": {
            "partner_sourced_trials": direct["trials"],
            "partner_sourced_paid_accounts": direct["paid_accounts"],
            "paid_seats": direct["seats"],
            "mrr": round(direct["mrr"], 2),
            "arr": round(direct["mrr"] * 12, 2),
            "note": "paid seats is the metric this system is judged on",
        },
        "best": best,
        "top_opportunities": _top(organizations, 5),
        "recommendations": learning.recommendations(analysis),
    }


def monthly(organizations, outreach, partners, attribution, days=30):
    analysis = learning.analyze(organizations, outreach, partners, attribution)
    org_index = {o["organization_id"]: o for o in organizations}
    archetypes = []
    attr_index = {a["organization_id"]: a for a in attribution}
    for p in partners:
        org = org_index.get(p.get("organization_id"))
        if org:
            archetypes.append(learning.archetype(p, org, attr_index.get(org["organization_id"])))

    per_partner = []
    for a in attribution:
        d = a.get("direct") or {}
        per_partner.append({
            "attribution_id": a["attribution_id"],
            "seats": d.get("seats", 0),
            "mrr": d.get("mrr", 0),
        })
    per_partner.sort(key=lambda r: r["seats"], reverse=True)

    return {
        "period_days": days,
        "analysis": analysis,
        "archetypes": archetypes,
        "seats_per_partner": per_partner,
        "observed_rates": _observed(attribution),
        "recommended_lookalikes": [learning.lookalike_query(a) for a in archetypes[:5]],
        "recommended_experiments": _experiments(analysis),
        "note": "the Learning Agent proposes; a human applies. Pricing, suppression, "
                "compliance and approved claims are not proposable.",
    }


def _observed(attribution):
    from . import attribution as attr_mod
    return attr_mod.observed_rates(attribution)


def _best(analysis):
    def top(mapping, key):
        if not mapping:
            return None
        ranked = sorted(mapping.items(), key=lambda kv: kv[1].get(key, 0), reverse=True)
        return ranked[0][0] if ranked and ranked[0][1].get(key, 0) else None

    return {
        "category_by_seats": top(analysis["by_category"], "seats"),
        "category_by_positive": top(analysis["by_category"], "positive"),
        "offer": top(analysis["offers"], "positive"),
    }


def _top(organizations, n):
    ranked = sorted([o for o in organizations if o.get("organization_score") is not None],
                    key=lambda o: o["organization_score"], reverse=True)
    return [{"organization_id": o["organization_id"],
             "name": o["organization_name"],
             "score": o["organization_score"],
             "band": o.get("priority_band"),
             "state": o.get("state"),
             "next_action": o.get("next_action")} for o in ranked[:n]]


def _experiments(analysis):
    out = []
    if analysis["unsignalled_outreach"] and analysis["signal_backed_outreach"]:
        out.append("signal-backed vs generic-relevance first touch")
    if len(analysis["offers"]) > 1:
        out.append("offer test: %s" % " vs ".join(sorted(analysis["offers"])[:3]))
    out.append("CTA test: useful-question close vs meeting request")
    out.append("contact role test: programs vs membership vs partnerships")
    out.append("audience framing test: members vs businesses vs community")
    return out
