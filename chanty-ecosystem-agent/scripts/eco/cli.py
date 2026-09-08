"""Command line for the deterministic core.

    python3 -m eco <command> [args]

Run from the project root, or anywhere: paths resolve from the package, not the
shell. Commands that change data print what they changed. Commands that would
send anything do not exist here, on purpose: sending is a human action taken
through the outreach workflow after the send gate passes.
"""

import argparse
import json
import os
import sys

from . import (attio, attribution, audit, dedupe, gates, gmail, ids, learning,
               paths, policy, report, response, scoring, state_machine, store,
               timezones, validate)


def _load_json_arg(value):
    if value is None:
        return None
    if value == "-":
        return json.load(sys.stdin)
    if os.path.exists(value):
        with open(value) as fh:
            return json.load(fh)
    return json.loads(value)


def _out(obj):
    print(json.dumps(obj, indent=2, sort_keys=True, default=str))


# --------------------------------------------------------------------------

def cmd_init(args):
    paths.ensure_dirs()
    audit.record(action="init", input={"root": paths.ROOT})
    _out({"ok": True, "root": paths.ROOT,
          "collections": sorted(paths.COLLECTIONS),
          "policy_version": policy.get("policy_version"),
          "autonomy_level": policy.autonomy_level(),
          "posture": policy.get("autonomy.default_posture")})


def cmd_policy(args):
    if args.key:
        _out({args.key: policy.get(args.key)})
    else:
        _out(policy.load())


def cmd_add_org(args):
    candidate = _load_json_arg(args.json)
    existing, reason = dedupe.find_duplicate(candidate)
    if existing:
        audit.record(action="dedupe_skip", agent="discovery",
                     organization=existing["organization_id"],
                     input={"name": candidate.get("organization_name")},
                     decision="duplicate by %s" % reason)
        _out({"created": False, "duplicate_of": existing["organization_id"],
              "reason": reason, "name": existing["organization_name"]})
        return

    record = dict(candidate)
    record["organization_id"] = dedupe.proposed_id(candidate)
    record.setdefault("state", "DISCOVERED")
    record.setdefault("state_history", [])
    record.setdefault("status", "unverified")
    record.setdefault("evidence", [])
    record.setdefault("industries", [])
    record.setdefault("contradictions", [])
    for k in ("trials", "paid_accounts", "seats", "mrr", "arr", "assisted_revenue"):
        record.setdefault(k, 0)
    record.setdefault("created_at", audit.now())
    record["updated_at"] = audit.now()
    if not record.get("domain"):
        record["domain"] = dedupe.normalize_domain(record.get("website"))
    store.put("organizations", record)
    _out({"created": True, "organization_id": record["organization_id"],
          "state": record["state"]})


def cmd_dedupe_check(args):
    candidate = _load_json_arg(args.json)
    existing, reason = dedupe.find_duplicate(candidate)
    _out({"duplicate": bool(existing), "reason": reason,
          "matched": existing["organization_id"] if existing else None,
          "would_be_id": dedupe.proposed_id(candidate)})


def cmd_score(args):
    org = store.get("organizations", args.org_id)
    if not org:
        sys.exit("no organization %s" % args.org_id)
    result = scoring.score(_load_json_arg(args.json))
    org.update({"organization_score": result["organization_score"],
                "priority_band": result["priority_band"],
                "score_breakdown": result["score_breakdown"],
                "updated_at": audit.now()})
    org["partner_tier"] = scoring.partner_tier(
        result["priority_band"], org.get("national_or_local"),
        bool(org.get("chapter") or org.get("parent_organization")),
        result["score_breakdown"])
    store.put("organizations", org)
    audit.record(action="score", agent="intelligence", organization=org["organization_id"],
                 output=result, decision=result["priority_band"])
    _out(result)


def cmd_gate(args):
    org = store.get("organizations", args.org_id)
    if not org:
        sys.exit("no organization %s" % args.org_id)
    contact = store.get("contacts", args.contact_id) if args.contact_id else None
    opp = store.get("opportunities", args.opportunity_id) if args.opportunity_id else None
    result = gates.check_qualification(org, contact, opp)
    org["qualification"] = result.to_dict()
    org["updated_at"] = audit.now()
    store.put("organizations", org)
    audit.record(action="qualification_gate", agent="intelligence",
                 organization=org["organization_id"], output=result.to_dict(),
                 decision="passed" if result.passed else "failed")
    _out(result.to_dict())


def cmd_transition(args):
    org = store.get("organizations", args.org_id)
    if not org:
        sys.exit("no organization %s" % args.org_id)
    context = _load_json_arg(args.context) or {}
    if args.event == "ready_for_outreach":
        context.setdefault("qualification_gates_passed",
                           bool((org.get("qualification") or {}).get("passed")))
    try:
        state_machine.apply(org, args.event, actor=args.actor, context=context,
                            target_state=args.target_state)
    except state_machine.TransitionError as exc:
        audit.record(action="state_transition_rejected", organization=args.org_id,
                     input={"event": args.event}, error=str(exc))
        sys.exit("blocked: %s" % exc)
    org["updated_at"] = audit.now()
    store.put("organizations", org)
    _out({"organization_id": org["organization_id"], "state": org["state"],
          "allowed_next": state_machine.allowed_events(org["state"])})


def cmd_add_contact(args):
    payload = _load_json_arg(args.json)
    payload.setdefault("contact_id", ids.make_id(
        "contacts", "%s|%s" % (payload.get("organization_id"), payload.get("full_name", "").lower())))
    payload.setdefault("created_at", audit.now())
    payload.setdefault("enrichment_used", False)
    payload.setdefault("suppressed", False)
    payload.setdefault("is_primary", True)
    payload.setdefault("sources_checked", [])
    payload.setdefault("alternative_contact_methods", [])
    payload.setdefault("response_history", [])
    payload.setdefault("requires_user_permission",
                       payload.get("email_status") != "public_verified")

    result = gates.check_contact_data_policy(payload)
    if not result.passed:
        audit.record(action="contact_rejected", agent="contact",
                     organization=payload.get("organization_id"),
                     output=result.to_dict(), error="contact data policy")
        _out({"created": False, "gate": result.to_dict()})
        sys.exit(2)

    sup = gates.check_suppression(store.get("organizations", payload["organization_id"]), payload)
    if not sup.passed:
        _out({"created": False, "gate": sup.to_dict()})
        sys.exit(2)

    store.put("contacts", payload)
    _out({"created": True, "contact_id": payload["contact_id"],
          "email_status": payload["email_status"],
          "requires_user_permission": payload["requires_user_permission"]})


def cmd_contact_report(args):
    """The EMAIL_NOT_PUBLIC handoff, in the exact shape the spec calls for."""
    contact = store.get("contacts", args.contact_id)
    if not contact:
        sys.exit("no contact %s" % args.contact_id)
    org = store.get("organizations", contact["organization_id"]) or {}
    print("CONTACT IDENTIFIED")
    print("Name: %s" % contact.get("full_name"))
    print("Title: %s" % (contact.get("title") or "unknown"))
    print("Organization: %s" % org.get("organization_name", contact["organization_id"]))
    if contact.get("email_status") == "public_verified":
        print("Public email: %s (%s)" % (contact["email"], contact.get("email_source_url")))
        return
    print("Public email: NOT FOUND")
    print("")
    print("Public sources checked:")
    for s in contact.get("sources_checked") or ["(none recorded)"]:
        print("- %s" % s)
    print("")
    print("Alternative public contact methods:")
    for s in contact.get("alternative_contact_methods") or ["(none found)"]:
        print("- %s" % s)
    print("")
    print("requires_user_permission = true")
    print("recommended_action = ASK_USER")
    print("enrichment_used = false")


def cmd_check_tool(args):
    result = gates.check_tool_permitted(args.tool)
    _out(result.to_dict())
    if not result.passed:
        sys.exit(3)


def cmd_add_signal(args):
    payload = _load_json_arg(args.json)
    payload.setdefault("signal_id", ids.make_id(
        "signals", "%s|%s|%s" % (payload.get("organization_id"), payload.get("summary"),
                                 payload.get("signal_date"))))
    payload.setdefault("created_at", audit.now())
    payload.setdefault("used_in_outreach", [])
    age = _age_days(payload.get("signal_date"))
    if age is not None:
        payload["decay_band"] = policy.signal_decay_band(age)
    store.put("signals", payload)
    _out({"created": True, "signal_id": payload["signal_id"],
          "decay_band": payload.get("decay_band"), "age_days": age})


def _age_days(date_str):
    import datetime
    if not date_str:
        return None
    try:
        when = datetime.datetime.fromisoformat(date_str)
    except ValueError:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=datetime.timezone.utc)
    return (datetime.datetime.now(datetime.timezone.utc) - when).days


def cmd_draft_check(args):
    draft = _load_json_arg(args.json)
    body = "\n".join(filter(None, [draft.get("subject"), draft.get("body")]))
    claims = gates.check_claims(body)
    personal = gates.check_personalization(body, draft.get("personalization_claims"))
    fmt = gates.check_format(draft.get("body"))
    delivery = gates.check_delivery_disclosure(draft.get("body"), draft.get("offer"))
    passed = claims.passed and personal.passed and fmt.passed and delivery.passed
    _out({"claims": claims.to_dict(), "personalization": personal.to_dict(),
          "format": fmt.to_dict(), "delivery_disclosure": delivery.to_dict(),
          "passed": passed})
    if not passed:
        sys.exit(2)


def cmd_gmail_draft(args):
    """Print the create_draft call for the agent to make. Creates nothing here."""
    draft = _load_json_arg(args.json)
    contact = store.get("contacts", draft["contact_id"])
    org = store.get("organizations", draft.get("organization_id"))
    if not contact:
        sys.exit("no contact %s" % draft.get("contact_id"))
    try:
        payload = gmail.plan(draft, contact, org)
    except gmail.DraftRejected as exc:
        audit.record(action="gmail_draft_rejected", agent="outreach",
                     organization=draft.get("organization_id"),
                     contact=draft.get("contact_id"), error=str(exc),
                     output=[r.to_dict() for r in exc.gate_results])
        _out({"ok": False, "reason": str(exc),
              "gates": [r.to_dict() for r in exc.gate_results]})
        sys.exit(2)
    audit.record(action="gmail_draft_planned", agent="outreach",
                 organization=draft.get("organization_id"),
                 contact=draft.get("contact_id"), output={"to": payload["args"]["to"]},
                 decision="ready for review in Gmail")
    _out(payload)


def cmd_send_check(args):
    draft = _load_json_arg(args.json)
    org = store.get("organizations", draft["organization_id"])
    contact = store.get("contacts", draft["contact_id"])
    opp = store.get("opportunities", draft.get("opportunity_id")) if draft.get("opportunity_id") else None
    if not org or not contact:
        sys.exit("organization or contact not found")
    when = None
    if getattr(args, "now", None):
        import datetime
        when = datetime.datetime.fromisoformat(args.now)
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
    result = gates.check_send(org, contact, draft, opp,
                              human_approved=args.human_approved, now=when)
    payload = result.to_dict()
    payload["sub_results"] = getattr(result, "sub_results", {})
    audit.record(action="send_gate", agent="outreach", organization=org["organization_id"],
                 contact=contact["contact_id"], output=payload,
                 decision="allowed" if result.passed else "blocked")
    _out(payload)
    if not result.passed:
        sys.exit(2)


def cmd_response(args):
    plan = response.plan(args.classification, args.body or "")
    _out(plan)


def cmd_attribution(args):
    org = store.get("organizations", args.org_id)
    if not org:
        sys.exit("no organization %s" % args.org_id)
    record = attribution.create(org)
    record["created_at"] = audit.now()
    store.put("attribution", record)
    org["attribution_id"] = record["attribution_id"]
    store.put("organizations", org)
    _out(record)


def cmd_forecast(args):
    _out(attribution.expected_paid_seats(args.audience,
                                         _load_json_arg(args.overrides)))


def cmd_backfill_timezones(args):
    """Resolve and store the local timezone for every organization."""
    changed = []
    for org in store.all("organizations"):
        name, conf = timezones.resolve(org.get("city"), org.get("state_region"),
                                       org.get("country") or "US")
        if org.get("timezone") == name and org.get("timezone_confidence") == conf:
            continue
        org["timezone"], org["timezone_confidence"] = name, conf
        org["updated_at"] = audit.now()
        store.put("organizations", org, log=False)
        changed.append({"organization": org["organization_name"],
                        "timezone": name, "confidence": conf})
    _out({"updated": len(changed), "organizations": changed})


def cmd_send_window(args):
    """When may this organization be emailed, and is that now."""
    rows = []
    orgs = ([store.get("organizations", args.org_id)] if args.org_id
            else store.all("organizations"))
    for org in orgs:
        if not org:
            sys.exit("no such organization")
        if args.drafts_only and org.get("state") != "READY_FOR_OUTREACH":
            continue
        gate = gates.check_send_window(org)
        window = gates.send_window(org)
        here = gates.local_now(org)
        nxt = gates.next_send_time(org)
        rows.append({
            "organization": org["organization_name"],
            "timezone": window["timezone"],
            "confidence": window["confidence"],
            "window_local": "%02d:00-%02d:00" % (window["start_hour"], window["end_hour"]),
            "their_local_time": here.strftime("%a %H:%M") if here else None,
            "sendable_now": gate.passed,
            "blocked_by": [f["check"] for f in gate.failures],
            "next_send_time_local": nxt.strftime("%a %d %b %H:%M %Z") if nxt else None,
        })
    _out(rows)


def cmd_report(args):
    orgs = store.all("organizations")
    out = store.all("outreach")
    sigs = store.all("signals")
    partners = store.all("partners")
    attrs = store.all("attribution")
    if args.period == "weekly":
        _out(report.weekly(orgs, out, sigs, partners, attrs))
    else:
        _out(report.monthly(orgs, out, partners, attrs))


def cmd_learn(args):
    analysis = learning.analyze(store.all("organizations"), store.all("outreach"),
                                store.all("partners"), store.all("attribution"))
    _out({"analysis": analysis, "recommendations": learning.recommendations(analysis)})


def cmd_attio_plan(args):
    org = store.get("organizations", args.org_id)
    if not org:
        sys.exit("no organization %s" % args.org_id)
    contacts = [c for c in store.all("contacts") if c["organization_id"] == org["organization_id"]]
    sigs = [s for s in store.all("signals") if s["organization_id"] == org["organization_id"]]
    opps = [o for o in store.all("opportunities") if o["organization_id"] == org["organization_id"]]
    _out(attio.plan(org, contacts, opps[0] if opps else None, sigs))


def cmd_status(args):
    orgs = store.all("organizations")
    by_state = {}
    for o in orgs:
        by_state[o.get("state")] = by_state.get(o.get("state"), 0) + 1
    _out({
        "organizations": len(orgs),
        "by_state": by_state,
        "contacts": len(store.all("contacts")),
        "contacts_email_not_public": len([c for c in store.all("contacts")
                                          if c.get("email_status") != "public_verified"]),
        "enrichment_used_count": len([c for c in store.all("contacts") if c.get("enrichment_used")]),
        "signals": len(store.all("signals")),
        "outreach_drafts": len([o for o in store.all("outreach") if o.get("status") == "draft"]),
        "outreach_sent": len([o for o in store.all("outreach") if o.get("status") == "sent"]),
        "partners": len(store.all("partners")),
        "suppressions": len(store.all("suppression")),
        "autonomy_level": policy.autonomy_level(),
        "posture": policy.get("autonomy.default_posture"),
        "audit_entries": len(audit.read()),
    })


def cmd_suppress(args):
    record = {
        "suppression_id": ids.make_id("suppression", "%s|%s" % (args.scope, args.value)),
        "scope": args.scope,
        "value": args.value,
        "reason": args.reason,
        "note": args.note,
        "permanent": True,
        "created_at": audit.now(),
        "created_by": args.by,
        "lifted_at": None,
        "lifted_by": None,
    }
    store.put("suppression", record)
    if args.scope == "contact":
        for c in store.all("contacts"):
            if args.value in (c.get("contact_id"), c.get("email")):
                c["suppressed"] = True
                c["suppression_id"] = record["suppression_id"]
                store.put("contacts", c)
    audit.record(action="suppress", input={"scope": args.scope, "value": args.value},
                 decision=args.reason, human_override=(args.by != "agent"))
    _out(record)


def cmd_validate(args):
    problems = []
    for collection in paths.COLLECTIONS:
        for record in store.all(collection):
            try:
                validate.validate(record, store.schema(collection))
            except validate.ValidationError as exc:
                problems.append({"collection": collection, "errors": exc.errors})
    _out({"valid": not problems, "problems": problems})
    if problems:
        sys.exit(2)


def cmd_audit(args):
    for entry in audit.read(limit=args.limit):
        print(json.dumps(entry, sort_keys=True))


def build_parser():
    p = argparse.ArgumentParser(prog="eco", description="Chanty Ecosystem Agent core")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    sp = sub.add_parser("policy"); sp.add_argument("key", nargs="?"); sp.set_defaults(func=cmd_policy)
    sp = sub.add_parser("status"); sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("add-org"); sp.add_argument("json"); sp.set_defaults(func=cmd_add_org)
    sp = sub.add_parser("dedupe-check"); sp.add_argument("json"); sp.set_defaults(func=cmd_dedupe_check)

    sp = sub.add_parser("score"); sp.add_argument("org_id"); sp.add_argument("json")
    sp.set_defaults(func=cmd_score)

    sp = sub.add_parser("gate"); sp.add_argument("org_id")
    sp.add_argument("--contact-id"); sp.add_argument("--opportunity-id")
    sp.set_defaults(func=cmd_gate)

    sp = sub.add_parser("transition"); sp.add_argument("org_id"); sp.add_argument("event")
    sp.add_argument("--actor", default="agent"); sp.add_argument("--context")
    sp.add_argument("--target-state"); sp.set_defaults(func=cmd_transition)

    sp = sub.add_parser("add-contact"); sp.add_argument("json"); sp.set_defaults(func=cmd_add_contact)
    sp = sub.add_parser("contact-report"); sp.add_argument("contact_id")
    sp.set_defaults(func=cmd_contact_report)
    sp = sub.add_parser("check-tool"); sp.add_argument("tool"); sp.set_defaults(func=cmd_check_tool)

    sp = sub.add_parser("add-signal"); sp.add_argument("json"); sp.set_defaults(func=cmd_add_signal)

    sp = sub.add_parser("draft-check"); sp.add_argument("json"); sp.set_defaults(func=cmd_draft_check)
    sp = sub.add_parser("gmail-draft"); sp.add_argument("json"); sp.set_defaults(func=cmd_gmail_draft)
    sp = sub.add_parser("send-check"); sp.add_argument("json")
    sp.add_argument("--human-approved", action="store_true")
    sp.add_argument("--now", help="ISO timestamp, to preview the gate at another moment")
    sp.set_defaults(func=cmd_send_check)

    sp = sub.add_parser("response"); sp.add_argument("classification")
    sp.add_argument("--body"); sp.set_defaults(func=cmd_response)

    sp = sub.add_parser("attribution"); sp.add_argument("org_id"); sp.set_defaults(func=cmd_attribution)
    sp = sub.add_parser("forecast"); sp.add_argument("audience", type=float)
    sp.add_argument("--overrides"); sp.set_defaults(func=cmd_forecast)

    sp = sub.add_parser("report"); sp.add_argument("period", choices=["weekly", "monthly"])
    sp.set_defaults(func=cmd_report)
    sub.add_parser("learn").set_defaults(func=cmd_learn)

    sp = sub.add_parser("attio-plan"); sp.add_argument("org_id"); sp.set_defaults(func=cmd_attio_plan)

    sp = sub.add_parser("suppress"); sp.add_argument("scope", choices=["contact", "organization", "domain"])
    sp.add_argument("value"); sp.add_argument("reason")
    sp.add_argument("--note"); sp.add_argument("--by", default="human")
    sp.set_defaults(func=cmd_suppress)

    sub.add_parser("backfill-timezones").set_defaults(func=cmd_backfill_timezones)
    sp = sub.add_parser("send-window"); sp.add_argument("org_id", nargs="?")
    sp.add_argument("--drafts-only", action="store_true"); sp.set_defaults(func=cmd_send_window)

    sub.add_parser("validate").set_defaults(func=cmd_validate)
    sp = sub.add_parser("audit"); sp.add_argument("--limit", type=int, default=20)
    sp.set_defaults(func=cmd_audit)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    paths.ensure_dirs()
    return args.func(args)


if __name__ == "__main__":
    main()
