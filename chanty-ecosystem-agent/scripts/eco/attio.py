"""Attio sync planning.

Attio is the system of record for operational relationship state. This module
does not call Attio: MCP tools live in the agent, not in Python. It produces an
explicit, reviewable plan of the calls to make, which the agent then executes
one at a time and records in the audit log.

The mapping below was built against the live Chanty workspace on 2026-09-07.
That workspace has the two standard objects (companies, people) and no custom
objects. The MCP surface cannot create objects or attributes, so the fields this
system needs that Attio does not have yet are listed in `missing_attributes`
rather than quietly dropped or crammed into a field that means something else.
"""

WORKSPACE = "Chanty"

COMPANY_OBJECT = "companies"
PERSON_OBJECT = "people"

# Verified writable attributes as of 2026-09-07.
COMPANY_FIELDS = {"name", "domains", "description", "linkedin", "primary_location",
                  "employee_range", "categories", "twitter", "facebook", "instagram",
                  "estimated_arr_usd", "funding_raised_usd", "foundation_date", "team"}
PERSON_FIELDS = {"name", "email_addresses", "job_title", "company", "linkedin",
                 "phone_numbers", "description", "primary_location", "stage",
                 "who_contacted", "twitter", "facebook", "instagram"}

# Ecosystem state has no home in the standard schema. These need a human to add
# them in the Attio UI (Settings > Objects > Companies > Attributes) before the
# sync can carry them as structured data instead of note text.
MISSING_COMPANY_ATTRIBUTES = [
    ("ecosystem_state", "status", "the state machine state"),
    ("organization_score", "number", "0-100"),
    ("priority_band", "select", "STRATEGIC / TIER_1 / TIER_2 / NURTURE / ARCHIVE"),
    ("organization_type", "select", "taxonomy type"),
    ("partner_tier", "select", "A / B / C / D"),
    ("attribution_id", "text", "CHANTY-... partner tracking id"),
    ("audience_size", "number", ""),
    ("audience_confidence", "select", "KNOWN_FACT / ESTIMATE / UNKNOWN"),
    ("recommended_offer", "select", "approved offers"),
    ("parent_organization", "record-reference", "chapter hierarchy"),
    ("last_researched", "date", ""),
]
MISSING_PERSON_ATTRIBUTES = [
    ("email_status", "select", "public_verified / not_publicly_found / org_inbox_only / form_only"),
    ("email_source_url", "text", "where the public email was read from"),
    ("role_category", "select", "partnerships / membership / programs / events / ..."),
]

ECOSYSTEM_LIST = {
    "name": "Ecosystem Partners",
    "api_slug": "ecosystem_partners",
    "parent_object": COMPANY_OBJECT,
}

EMPLOYEE_RANGES = ["1-10", "11-50", "51-250", "251-1K", "1K-5K", "5K-10K",
                   "10K-50K", "50K-100K", "100K+"]


def company_values(org):
    """Only fields that exist and are writable. Nothing invented."""
    values = {"name": org["organization_name"]}
    domain = org.get("domain")
    if domain:
        values["domains"] = [domain]
    if org.get("linkedin"):
        values["linkedin"] = org["linkedin"]
    if org.get("audience_description"):
        values["description"] = _describe(org)
    location = ", ".join(p for p in [org.get("city"), org.get("state_region"),
                                     org.get("country")] if p)
    if location:
        values["primary_location"] = location
    return values


def _describe(org):
    """Description carries the human-readable summary, with confidence intact."""
    bits = [org.get("audience_description")]
    if org.get("audience_size") and org.get("audience_confidence") == "KNOWN_FACT":
        bits.append("Stated audience: %s %s." % (org["audience_size"],
                                                 org.get("audience_size_type") or ""))
    elif org.get("audience_size"):
        bits.append("Estimated audience (not stated by the organization): %s %s."
                    % (org["audience_size"], org.get("audience_size_type") or ""))
    return " ".join(b.strip() for b in bits if b)[:1000]


def person_values(contact, company_domain=None):
    """A person record is only created when the email is public.

    A contact whose email is not public stays out of Attio's people object; it
    lives in the local store as EMAIL_NOT_PUBLIC awaiting a human decision.
    """
    if contact.get("email_status") != "public_verified":
        raise ValueError("refusing to sync a person without a public verified email")

    values = {
        "name": _personal_name(contact),
        "email_addresses": [contact["email"]],
    }
    if contact.get("title"):
        values["job_title"] = contact["title"]
    if contact.get("public_profile_url"):
        values["linkedin"] = contact["public_profile_url"]
    if contact.get("public_phone"):
        values["phone_numbers"] = [contact["public_phone"]]
    if company_domain:
        values["company"] = company_domain
    return values


def _personal_name(contact):
    first = contact.get("first_name")
    last = contact.get("last_name")
    if first and last:
        return [{"first_name": first, "last_name": last,
                 "full_name": contact["full_name"]}]
    parts = contact["full_name"].split()
    if len(parts) >= 2:
        return [{"first_name": parts[0], "last_name": " ".join(parts[1:]),
                 "full_name": contact["full_name"]}]
    return [{"first_name": contact["full_name"], "last_name": "",
             "full_name": contact["full_name"]}]


def note_body(org, contacts=None, opportunity=None, signals=None):
    """The structured fields Attio cannot hold yet, written as one readable note.

    Verbose on purpose: until the custom attributes exist, this note is the only
    place a person in Attio can see why an organization scored what it scored.
    """
    lines = ["Chanty Ecosystem Agent record", ""]
    lines.append("State: %s" % org.get("state"))
    lines.append("Score: %s (%s)" % (org.get("organization_score"), org.get("priority_band")))
    lines.append("Type: %s" % org.get("organization_type"))
    if org.get("partner_tier"):
        lines.append("Partner tier: %s" % org["partner_tier"])
    if org.get("attribution_id"):
        lines.append("Attribution ID: %s" % org["attribution_id"])

    size = org.get("audience_size")
    if size:
        lines.append("Audience: %s %s (%s)" % (size, org.get("audience_size_type") or "",
                                               org.get("audience_confidence")))
    mechanisms = [k for k, v in (org.get("distribution") or {}).items()
                  if isinstance(v, dict) and v.get("present")]
    if mechanisms:
        lines.append("Distribution: %s" % ", ".join(sorted(mechanisms)))

    if opportunity:
        lines += ["", "Recommended offer: %s" % opportunity.get("recommended_offer"),
                  "Why: %s" % (opportunity.get("why_this_offer") or "not recorded"),
                  "Why now: %s" % (opportunity.get("why_now") or "no current trigger")]

    if signals:
        lines += ["", "Signals:"]
        for s in signals[:5]:
            lines.append("- %s (%s, %s) %s" % (s.get("summary"), s.get("signal_date"),
                                               s.get("decay_band"), s.get("source_url")))

    if contacts:
        lines += ["", "Contacts:"]
        for c in contacts:
            lines.append("- %s, %s [%s]" % (c.get("full_name"), c.get("title") or "title unknown",
                                            c.get("email_status")))
            if c.get("email_status") != "public_verified":
                lines.append("  no public email found; awaiting user decision. "
                             "Sources checked: %s" % ", ".join(c.get("sources_checked") or []))

    evidence = org.get("evidence") or []
    if evidence:
        lines += ["", "Evidence:"]
        for e in evidence[:10]:
            lines.append("- [%s] %s - %s (checked %s)" % (e.get("source_type"), e.get("claim"),
                                                          e.get("source_url"), e.get("date_checked")))
    if org.get("contradictions"):
        lines += ["", "Unresolved contradictions:"] + ["- " + c for c in org["contradictions"]]

    lines += ["", "No enrichment provider was used for any contact on this record."]
    return "\n".join(lines)


def plan(org, contacts=None, opportunity=None, signals=None):
    """An ordered list of MCP calls for the agent to execute after approval."""
    contacts = contacts or []
    calls = [{
        "tool": "mcp__Attio__upsert-record",
        "why": "organization is the system-of-record company",
        "args": {
            "object": COMPANY_OBJECT,
            "matching_attribute": "domains" if org.get("domain") else "name",
            "values": company_values(org),
        },
    }]

    for c in contacts:
        if c.get("email_status") != "public_verified":
            calls.append({
                "tool": None,
                "skipped": True,
                "why": "%s has email_status=%s; no person record is created and no "
                       "enrichment is attempted" % (c.get("full_name"), c.get("email_status")),
            })
            continue
        calls.append({
            "tool": "mcp__Attio__upsert-record",
            "why": "public verified contact",
            "args": {
                "object": PERSON_OBJECT,
                "matching_attribute": "email_addresses",
                "values": person_values(c, org.get("domain")),
            },
        })

    calls.append({
        "tool": "mcp__Attio__create-note",
        "why": "carries the fields Attio has no attributes for yet",
        "args": {
            "parent_object": COMPANY_OBJECT,
            "parent_record_id": "<company record_id from the upsert above>",
            "title": "Ecosystem: %s (%s)" % (org["organization_name"], org.get("priority_band")),
            "content": note_body(org, contacts, opportunity, signals),
        },
    })

    return {
        "organization_id": org["organization_id"],
        "calls": calls,
        "missing_attributes": {
            "companies": MISSING_COMPANY_ATTRIBUTES,
            "people": MISSING_PERSON_ATTRIBUTES,
        },
        "requires_human_approval": True,
        "note": "Nothing here runs automatically. The agent executes these calls "
                "only after the user approves writing to Attio.",
    }
