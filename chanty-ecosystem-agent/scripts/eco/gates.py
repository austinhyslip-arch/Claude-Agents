"""Gates. Everything here fails closed.

Three families:
  1. Contact data policy - can this contact even be used, and was it obtained
     the way policy requires.
  2. Hard qualification gates - may this organization enter outreach at all.
  3. Send gates - may this specific message leave.

A gate returns a GateResult. `passed` is only true when every check passed and
no check errored. Absence of evidence is a failure, not a pass.
"""

import datetime
import re
from zoneinfo import ZoneInfo

from . import policy, store, timezones

# Patterns that indicate a constructed rather than discovered address. These
# catch the common mechanical forms; the real defence is that a contact record
# without a source URL fails regardless of what the address looks like.
_GUESS_HINTS = ("guess", "pattern", "inferred", "constructed", "assumed", "likely")

_PRICE_RE = re.compile(r"\$\s*(\d+(?:\.\d+)?)")

_PROHIBITED_PHRASES = [
    "discount", "% off", "percent off", "special pricing", "special rate",
    "member pricing", "member rate", "exclusive pricing", "exclusive rate",
    "preferred pricing", "preferred rate", "reduced rate", "promo", "promotional",
    "free account", "free accounts", "free seats", "comped", "no charge",
    "extended trial", "custom trial", "commission", "referral fee", "rev share",
    "revenue share", "revenue-share", "kickback", "spiff", "exclusivity",
    "exclusive partner", "limited spots", "limited time", "this month only",
    "act now", "closing soon", "last chance", "big fan of", "love what you're doing",
    "i've been following you for years",
]

_REGULATED_TOPICS = ["hipaa", "soc 2", "soc2", "gdpr", "data processing agreement",
                     "dpa", "data residency", "penetration test", "baa"]


class GateResult:
    def __init__(self, name):
        self.name = name
        self.checks = []

    def add(self, check, passed, detail=""):
        self.checks.append({"check": check, "passed": bool(passed), "detail": detail})
        return self

    @property
    def failures(self):
        return [c for c in self.checks if not c["passed"]]

    @property
    def passed(self):
        return bool(self.checks) and not self.failures

    def to_dict(self):
        return {
            "gate": self.name,
            "passed": self.passed,
            "checks": self.checks,
            "failures": [c["check"] for c in self.failures],
        }

    def __repr__(self):
        return "<GateResult %s passed=%s failures=%s>" % (
            self.name, self.passed, [c["check"] for c in self.failures])


# --------------------------------------------------------------------------
# 1. Contact data policy
# --------------------------------------------------------------------------

def check_contact_data_policy(contact, policy_path=None):
    g = GateResult("contact_data_policy")
    cdp = policy.get("contact_data_policy", {}, path=policy_path)
    permitted = set(cdp.get("permitted_public_sources", []))

    used_enrichment = bool(contact.get("enrichment_used"))
    authorized = contact.get("enrichment_authorized_by")
    g.add("no_unauthorized_enrichment", (not used_enrichment) or bool(authorized),
          "enrichment_used=%s authorized_by=%s" % (used_enrichment, authorized))

    email = (contact.get("email") or "").strip()
    status = contact.get("email_status")

    if status == "public_verified":
        g.add("email_present", bool(email), "email is required when status is public_verified")
        g.add("email_shape", bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)), email or "(empty)")
        g.add("email_has_source_url", bool(contact.get("email_source_url")),
              "a public email must carry the URL it was read from")
        method = contact.get("email_discovery_method")
        g.add("email_source_permitted", method in permitted, "method=%r" % method)
        g.add("email_source_type_not_D", contact.get("email_source_type") in ("A", "B", "C"),
              "source_type=%r" % contact.get("email_source_type"))
        g.add("email_date_checked", bool(contact.get("email_date_checked")), "")
        blob = " ".join(str(contact.get(k) or "") for k in
                        ("email_discovery_method", "email_source_url", "notes")).lower()
        g.add("no_guess_markers", not any(h in blob for h in _GUESS_HINTS), "")
    else:
        g.add("no_email_without_public_status", not email,
              "email_status=%r must not carry an address" % status)
        g.add("requires_user_permission_set",
              bool(contact.get("requires_user_permission")) or status == "suppressed",
              "a contact without a public email must be escalated to the user")

    g.add("not_suppressed", not contact.get("suppressed"), "")
    return g


def check_tool_permitted(tool_name, policy_path=None):
    """Called before any tool that could touch contact data."""
    g = GateResult("tool_permission")
    blocked = policy.blocked_tool(tool_name, path=policy_path)
    g.add("tool_not_blocked_for_contact_data", not blocked, tool_name)
    if blocked:
        g.add("enrichment_globally_allowed", policy.enrichment_allowed(path=policy_path),
              "policy.contact_data_policy.enrichment_allowed")
    return g


# --------------------------------------------------------------------------
# 2. Suppression
# --------------------------------------------------------------------------

def _domain_of(email_or_url):
    if not email_or_url:
        return None
    if "@" in email_or_url:
        return email_or_url.split("@")[-1].strip().lower()
    from .dedupe import normalize_domain
    return normalize_domain(email_or_url)


def check_suppression(organization=None, contact=None, root=None, suppressions=None):
    g = GateResult("suppression")
    records = suppressions if suppressions is not None else store.all("suppression", root)
    active = [s for s in records if not s.get("lifted_at")]

    org_id = (organization or {}).get("organization_id")
    con_id = (contact or {}).get("contact_id")
    email = (contact or {}).get("email")
    domains = {d for d in [
        _domain_of(email),
        _domain_of((organization or {}).get("domain") or (organization or {}).get("website")),
    ] if d}

    hits = []
    for s in active:
        if s["scope"] == "contact" and con_id and s["value"] in (con_id, email):
            hits.append(s)
        elif s["scope"] == "organization" and org_id and s["value"] == org_id:
            hits.append(s)
        elif s["scope"] == "domain" and s["value"].lower() in domains:
            hits.append(s)

    g.add("no_active_suppression", not hits,
          "; ".join("%s:%s (%s)" % (h["scope"], h["value"], h["reason"]) for h in hits))
    if contact is not None:
        g.add("contact_flag_clear", not contact.get("suppressed"), "")
    return g


# --------------------------------------------------------------------------
# 3. Hard qualification gates
# --------------------------------------------------------------------------

def check_qualification(organization, contact=None, opportunity=None, root=None,
                        suppressions=None):
    g = GateResult("hard_qualification")

    g.add("organization_verified", organization.get("status") == "active"
          and bool(organization.get("website")),
          "status=%r website=%r" % (organization.get("status"), organization.get("website")))

    g.add("audience_relevant", organization.get("smb_fit") in ("high", "medium")
          and bool(organization.get("audience_description")),
          "smb_fit=%r" % organization.get("smb_fit"))

    mechanisms = [k for k, v in (organization.get("distribution") or {}).items()
                  if isinstance(v, dict) and v.get("present")]
    g.add("distribution_mechanism_identified", bool(mechanisms),
          "mechanisms=%s" % (mechanisms or "none"))

    if contact is None:
        g.add("credible_contact_identified", False, "no contact record")
    else:
        cdp = check_contact_data_policy(contact)
        g.add("credible_contact_identified",
              cdp.passed and contact.get("email_status") == "public_verified"
              and bool(contact.get("title")),
              "contact_data_policy failures=%s" % [c["check"] for c in cdp.failures])

    hypothesis_ok = bool(opportunity) and bool(opportunity.get("why_this_offer")) \
        and bool(opportunity.get("distribution_mechanism")) \
        and opportunity.get("recommended_offer") in policy.get("approved_offers", [])
    g.add("partnership_hypothesis_exists", hypothesis_ok, "")

    evidence = organization.get("evidence") or []
    strong = [e for e in evidence if e.get("source_type") in ("A", "B", "C")]
    g.add("evidence_exists", len(strong) >= 2,
          "%d evidence items, %d at A/B/C" % (len(evidence), len(strong)))

    sup = check_suppression(organization, contact, root=root, suppressions=suppressions)
    g.add("no_suppression", sup.passed, "; ".join(c["detail"] for c in sup.failures))

    g.add("no_material_contradiction", not (organization.get("contradictions") or []),
          "; ".join(organization.get("contradictions") or []))
    return g


# --------------------------------------------------------------------------
# 4. Claims, pricing, personalization
# --------------------------------------------------------------------------

def check_claims(text, policy_path=None):
    g = GateResult("claims")
    lowered = (text or "").lower()

    found = [p for p in _PROHIBITED_PHRASES if p in lowered]
    g.add("no_prohibited_phrases", not found, ", ".join(found))

    price = policy.price_per_seat(path=policy_path)
    prices = [float(m) for m in _PRICE_RE.findall(lowered)]
    wrong = [p for p in prices if abs(p - price) > 1e-9]
    g.add("no_unauthorized_price", not wrong,
          "found %s, policy price is $%s" % (wrong, price))

    regulated = [t for t in _REGULATED_TOPICS if t in lowered]
    g.add("no_regulated_topic_claims", not regulated, ", ".join(regulated))

    return g


def check_personalization(text, evidence, min_source_type=("A", "B", "C")):
    """Every personalization claim must point at evidence we actually hold.

    evidence is the list attached to the draft: each item needs a claim, a
    source_url and a source_type. D-level evidence is discovery-only and cannot
    support a sentence in a message.
    """
    g = GateResult("personalization")
    evidence = evidence or []
    g.add("has_evidence", bool(evidence), "a personalized message needs at least one sourced claim")

    bad_type = [e.get("claim") for e in evidence if e.get("source_type") not in min_source_type]
    g.add("no_D_level_evidence", not bad_type, "; ".join(str(c) for c in bad_type))

    missing_url = [e.get("claim") for e in evidence if not e.get("source_url")]
    g.add("every_claim_has_source_url", not missing_url, "; ".join(str(c) for c in missing_url))

    estimates_stated_as_fact = [
        e.get("claim") for e in evidence
        if e.get("confidence") == "ESTIMATE" and _states_estimate_as_fact(text, e)
    ]
    g.add("no_estimate_stated_as_fact", not estimates_stated_as_fact,
          "; ".join(str(c) for c in estimates_stated_as_fact))
    return g


def _states_estimate_as_fact(text, evidence_item):
    """An estimated number must not appear as a bare figure in the message.

    "your 2,500 members" is a claim. "your member community" is not.
    """
    claim = str(evidence_item.get("claim") or "")
    numbers = re.findall(r"\d[\d,]{2,}", claim)
    lowered = (text or "").lower()
    for n in numbers:
        bare = n.replace(",", "")
        if n.lower() in lowered or bare in lowered.replace(",", ""):
            return True
    return False



# --------------------------------------------------------------------------
# 4b. Format: plain text, no sign-off
# --------------------------------------------------------------------------

_MARKDOWN_PATTERNS = [
    (r"\*\*[^*]+\*\*", "bold markers"),
    (r"(?m)^\s*#{1,6}\s", "markdown heading"),
    (r"(?m)^\s*[-*+]\s+\S", "bullet list"),
    (r"(?m)^\s*\d+[.)]\s+\S", "numbered list"),
    (r"\[[^\]]+\]\([^)]+\)", "markdown link"),
    (r"(?m)^\s*>\s", "blockquote"),
    (r"`[^`]+`", "code ticks"),
    (r"(?m)^\s*[-=_]{3,}\s*$", "horizontal rule"),
    (r"<[a-zA-Z/][^>]*>", "html tag"),
]


def check_format(body, policy_path=None):
    """Gmail supplies the signature and the formatting. The body supplies neither.

    A draft ends on its last real sentence. No closer, no name, no title, no
    links block, no markdown, no HTML.
    """
    g = GateResult("format")
    fmt = policy.get("email_format", {}, path=policy_path)
    text = body or ""

    g.add("has_body", bool(text.strip()), "")

    if fmt.get("markdown_allowed") is False:
        found = [label for pattern, label in _MARKDOWN_PATTERNS if re.search(pattern, text)]
        g.add("no_markdown_or_html", not found, ", ".join(found))

    if fmt.get("sign_off_allowed") is False:
        g.add("no_sign_off", not _has_sign_off(text, fmt.get("banned_sign_offs", [])),
              "the last lines read as a closer; Gmail adds the signature")

    g.add("no_unsubscribe_token", "{{unsubscribe" not in text and "{{opt_out" not in text,
          "a one-to-one Gmail message carries no unsubscribe token")
    return g


def _has_sign_off(text, banned):
    """Look only at the tail. "Thanks for the pointer" mid-message is fine."""
    lines = [ln.strip() for ln in (text or "").strip().splitlines() if ln.strip()]
    for line in lines[-3:]:
        stripped = line.rstrip(",.!-\u2014 ").lower()
        if stripped in banned:
            return True
        # "Best," followed by a name on the next line, or "Thanks, Austin".
        for closer in banned:
            if stripped.startswith(closer + ",") or stripped == closer:
                return True
    return False



# --------------------------------------------------------------------------
# 4c. Delivery constraints
# --------------------------------------------------------------------------

def check_delivery_disclosure(body, offer, policy_path=None):
    """A live session offer has to say we join remotely.

    We do not travel. An organization slotting us into a room expects a person
    in that room, so leaving it out means the first message misrepresents what
    they are agreeing to. Saying it up front costs a sentence. Saying it after
    they say yes costs the booking.

    Written resources and co-branded content carry no such constraint, so the
    check only applies to the offers named in policy.
    """
    g = GateResult("delivery_disclosure")
    dc = policy.get("delivery_constraints", {}, path=policy_path)

    if not dc.get("live_sessions_are_remote_only"):
        g.add("no_constraint_configured", True, "")
        return g

    if offer not in dc.get("offers_requiring_disclosure", []):
        g.add("offer_needs_no_disclosure", True, "offer=%r" % offer)
        return g

    lowered = (body or "").lower()
    phrases = dc.get("disclosure_phrases", [])
    g.add("states_remote_delivery", any(p in lowered for p in phrases),
          "a %r offer must say we join remotely" % offer)
    return g


# --------------------------------------------------------------------------
# 4d. Send window
# --------------------------------------------------------------------------

def organization_timezone(organization):
    """The organization's zone, from the record if stored, resolved if not."""
    name = organization.get("timezone")
    if name:
        return name, organization.get("timezone_confidence") or "KNOWN_FACT"
    return timezones.resolve(organization.get("city"), organization.get("state_region"),
                             organization.get("country") or "US")


def send_window(organization, policy_path=None):
    """The hours this organization may be emailed, and the zone defining them.

    Three outcomes:
      KNOWN_FACT        their zone, 08:00-17:00 local
      ESTIMATE          their likely zone, narrowed an hour each side so an hour
                        of error cannot push a message outside their day
      UNKNOWN_FALLBACK  no zone resolved, so noon Central, which is 10:00
                        Pacific and 13:00 Eastern and therefore inside the
                        working day whichever US zone they turn out to be in
    """
    cfg = policy.get("send_window", {}, path=policy_path)
    name, confidence = organization_timezone(organization)
    start = cfg.get("start_hour_local", 8)
    end = cfg.get("end_hour_local", 17)
    weekdays_only = cfg.get("weekdays_only", True)

    if not name:
        fb = cfg.get("unknown_timezone_fallback", {})
        country = (organization.get("country") or "US").upper()
        non_us = country not in ("US", "USA", "UNITED STATES")
        if fb.get("enabled") and (fb.get("applies_to_non_us", True) or not non_us):
            return {"timezone": fb.get("timezone", "America/Chicago"),
                    "confidence": "UNKNOWN_FALLBACK",
                    "start_hour": fb.get("start_hour_local", 12),
                    "end_hour": fb.get("end_hour_local", 13),
                    "weekdays_only": weekdays_only, "is_fallback": True}
        return {"timezone": None, "confidence": "UNKNOWN",
                "start_hour": start, "end_hour": end,
                "weekdays_only": weekdays_only, "is_fallback": False}

    if confidence == "ESTIMATE":
        pad = cfg.get("narrow_hours_when_timezone_estimated", 1)
        start, end = start + pad, end - pad
    return {"timezone": name, "confidence": confidence,
            "start_hour": start, "end_hour": end,
            "weekdays_only": weekdays_only, "is_fallback": False}


def local_now(organization, now=None, policy_path=None):
    """Now, in whichever zone the send window is measured in."""
    name = send_window(organization, policy_path=policy_path)["timezone"]
    if not name:
        return None
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)
    try:
        return now.astimezone(ZoneInfo(name))
    except Exception:
        return None


def check_send_window(organization, now=None, policy_path=None):
    """Block a send that would land outside the recipient's working day."""
    g = GateResult("send_window")
    cfg = policy.get("send_window", {}, path=policy_path)
    window = send_window(organization, policy_path=policy_path)

    if not window["timezone"]:
        g.add("timezone_known", False,
              "no timezone for %s, %s and the fallback does not apply here"
              % (organization.get("city"), organization.get("state_region")))
        return g

    if window["is_fallback"]:
        g.add("timezone_known", True,
              "zone unresolved for %s, %s; using the noon Central fallback"
              % (organization.get("city"), organization.get("state_region")))
    else:
        g.add("timezone_known", True, "%s (%s)" % (window["timezone"], window["confidence"]))

    here = local_now(organization, now, policy_path=policy_path)
    if here is None:
        g.add("local_time_resolvable", False, window["timezone"])
        return g

    if window["weekdays_only"]:
        g.add("is_a_weekday", here.weekday() in cfg.get("weekdays", [0, 1, 2, 3, 4]),
              "local day is %s" % here.strftime("%A"))

    g.add("within_business_hours",
          window["start_hour"] <= here.hour < window["end_hour"],
          "%s is %s, window is %02d:00-%02d:00%s"
          % (window["timezone"], here.strftime("%H:%M"),
             window["start_hour"], window["end_hour"],
             " (fallback)" if window["is_fallback"] else ""))
    return g


def next_send_time(organization, now=None, policy_path=None):
    """The next moment this organization may be emailed, in the window's zone."""
    window = send_window(organization, policy_path=policy_path)
    if not window["timezone"]:
        return None
    here = local_now(organization, now, policy_path=policy_path)
    if here is None:
        return None
    cfg = policy.get("send_window", {}, path=policy_path)
    days = cfg.get("weekdays", [0, 1, 2, 3, 4])
    candidate = here
    for _ in range(14):
        ok_day = (not window["weekdays_only"]) or candidate.weekday() in days
        if ok_day and candidate.hour < window["start_hour"]:
            return candidate.replace(hour=window["start_hour"], minute=0,
                                     second=0, microsecond=0)
        if ok_day and window["start_hour"] <= candidate.hour < window["end_hour"]:
            return candidate
        candidate = (candidate + datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0)
    return None



# --------------------------------------------------------------------------
# 5. Send gate
# --------------------------------------------------------------------------

def check_recent_outreach(contact, outreach_records=None, root=None, policy_path=None,
                          now=None):
    g = GateResult("recent_outreach")
    records = outreach_records if outreach_records is not None else store.all("outreach", root)
    mine = [o for o in records if o.get("contact_id") == contact.get("contact_id")]
    sent = [o for o in mine if o.get("status") == "sent"]

    max_touches = policy.max_touches(path=policy_path)
    g.add("under_max_touches", len(sent) < max_touches,
          "%d of %d touches already sent" % (len(sent), max_touches))

    responded = [o for o in mine if o.get("response_classification")
                 and o.get("response_classification") not in ("OOO",)]
    g.add("no_response_yet", not responded,
          "a reply stops automation: %s" % [o.get("response_classification") for o in responded])

    now = now or datetime.datetime.now(datetime.timezone.utc)
    min_gap = policy.get("min_days_between_touches", 3, path=policy_path)
    too_soon = []
    for o in sent:
        stamp = o.get("sent_at")
        if not stamp:
            continue
        try:
            when = datetime.datetime.fromisoformat(stamp)
        except ValueError:
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        if (now - when).days < min_gap:
            too_soon.append(stamp)
    g.add("respects_min_gap", not too_soon, "sent %s, minimum gap is %d days" % (too_soon, min_gap))
    return g


def check_compliance_configured(policy_path=None):
    """Requirements depend on how the mail actually goes out.

    In `manual_gmail_draft` mode a person reads each message and sends it
    himself, one to one, from his own mailbox. A postal address block and an
    unsubscribe link are requirements for bulk commercial mail and are not
    required here. Suppression still is: an opt-out arrives as a reply and gets
    honoured the same day.

    Change `sending_mode` to a bulk platform and both requirements come back,
    because the policy file, not this function, decides.
    """
    g = GateResult("email_compliance")
    ec = policy.get("email_compliance", {}, path=policy_path)

    g.add("sending_infrastructure_set", bool(ec.get("sending_infrastructure")),
          "policy.email_compliance.sending_infrastructure is null")
    g.add("legal_review_done", ec.get("legal_review_status") == "reviewed",
          "legal_review_status=%r" % ec.get("legal_review_status"))
    g.add("truthful_sender_identity", bool(ec.get("sender_identity_must_be_truthful")), "")
    g.add("suppression_is_centralized", bool(ec.get("centralized_suppression_required")), "")

    if ec.get("physical_address_required"):
        g.add("physical_address_set", bool(ec.get("physical_address")),
              "physical_address is required in %r mode and is null" % ec.get("sending_mode"))
    if ec.get("opt_out_link_required"):
        g.add("opt_out_configured", bool(ec.get("opt_out_link_token")),
              "opt_out_link_token is required in %r mode and is null" % ec.get("sending_mode"))
    else:
        g.add("opt_out_honored_on_reply", bool(ec.get("opt_out_honored_on_reply")),
              "a request to stop must be honoured even without an unsubscribe link")
    return g


def check_send(organization, contact, draft, opportunity=None, root=None,
               outreach_records=None, suppressions=None, policy_path=None,
               human_approved=False, now=None):
    """The last gate before anything leaves. Every sub-gate must pass."""
    g = GateResult("send")
    body = "\n".join(filter(None, [draft.get("subject"), draft.get("body")]))

    sub = {
        "hard_qualification": check_qualification(organization, contact, opportunity,
                                                  root=root, suppressions=suppressions),
        "contact_data_policy": check_contact_data_policy(contact, policy_path=policy_path),
        "suppression": check_suppression(organization, contact, root=root,
                                         suppressions=suppressions),
        "claims": check_claims(body, policy_path=policy_path),
        "personalization": check_personalization(body, draft.get("personalization_claims")),
        "recent_outreach": check_recent_outreach(contact, outreach_records, root=root,
                                                 policy_path=policy_path, now=now),
        "email_compliance": check_compliance_configured(policy_path=policy_path),
        "format": check_format(draft.get("body"), policy_path=policy_path),
        "delivery_disclosure": check_delivery_disclosure(draft.get("body"), draft.get("offer"),
                                                         policy_path=policy_path),
        "send_window": check_send_window(organization, now=now, policy_path=policy_path),
    }
    for name, result in sub.items():
        g.add(name, result.passed, ", ".join(c["check"] for c in result.failures))

    g.add("email_publicly_available", contact.get("email_status") == "public_verified",
          "email_status=%r" % contact.get("email_status"))

    offer = draft.get("offer")
    g.add("offer_approved", offer in policy.get("approved_offers", [], path=policy_path),
          "offer=%r" % offer)

    if policy.get("email_compliance.opt_out_link_required", False, path=policy_path):
        token = policy.get("email_compliance.opt_out_link_token", "", path=policy_path)
        g.add("opt_out_present", bool(token) and token in (draft.get("body") or ""),
              "this sending mode requires the opt-out token in the body")

    escalation = bool(draft.get("escalation_required")) or bool(
        (opportunity or {}).get("escalation_required"))
    g.add("no_pending_escalation", not escalation, "")

    permitted, why = _send_permission(organization, human_approved, policy_path)
    g.add("autonomy_or_human_approval", permitted, why)

    g.sub_results = {k: v.to_dict() for k, v in sub.items()}
    return g


def _send_permission(organization, human_approved, policy_path):
    from . import state_machine
    if human_approved:
        tier = organization.get("partner_tier")
        if tier == "A" or organization.get("priority_band") == "STRATEGIC":
            return True, "human approved a tier A organization"
        return True, "human approved"
    return state_machine.outreach_permitted(organization, policy_path=policy_path)
