"""Explicit state machine.

An LLM never sets a state. It emits an event; this module decides whether that
event is legal from the current state and what the resulting state is. An
illegal transition raises. There is no "close enough".

Some transitions carry a guard: a record cannot reach READY_FOR_OUTREACH unless
the hard qualification gates passed, and nothing reaches OUTREACH_ACTIVE unless
a human approved it at the current autonomy level.
"""

from . import audit, policy

STATES = [
    "DISCOVERED",
    "RESEARCHING",
    "QUALIFIED",
    "CONTACT_IDENTIFIED",
    "READY_FOR_OUTREACH",
    "OUTREACH_ACTIVE",
    "RESPONSE_RECEIVED",
    "HUMAN_REVIEW",
    "CONVERSATION",
    "PARTNERSHIP_NEGOTIATION",
    "PARTNER_WON",
    "ACTIVATION",
    "LIVE",
    "ATTRIBUTION",
    "NURTURE",
    "SUPPRESSED",
    "DISQUALIFIED",
    "EMAIL_NOT_PUBLIC",
]

TERMINAL = {"SUPPRESSED"}

# event -> (allowed from states, resulting state)
TRANSITIONS = {
    "start_research":        (["DISCOVERED", "NURTURE"], "RESEARCHING"),
    "qualify":               (["RESEARCHING"], "QUALIFIED"),
    "disqualify":            (["DISCOVERED", "RESEARCHING", "QUALIFIED", "CONTACT_IDENTIFIED",
                               "READY_FOR_OUTREACH", "EMAIL_NOT_PUBLIC", "NURTURE"], "DISQUALIFIED"),
    "nurture":               (["RESEARCHING", "QUALIFIED", "CONTACT_IDENTIFIED", "READY_FOR_OUTREACH",
                               "OUTREACH_ACTIVE", "RESPONSE_RECEIVED", "HUMAN_REVIEW",
                               "CONVERSATION", "EMAIL_NOT_PUBLIC"], "NURTURE"),
    "identify_contact":      (["QUALIFIED", "EMAIL_NOT_PUBLIC"], "CONTACT_IDENTIFIED"),
    "contact_email_not_public": (["QUALIFIED", "CONTACT_IDENTIFIED"], "EMAIL_NOT_PUBLIC"),
    "ready_for_outreach":    (["CONTACT_IDENTIFIED"], "READY_FOR_OUTREACH"),
    "start_outreach":        (["READY_FOR_OUTREACH"], "OUTREACH_ACTIVE"),
    "response_received":     (["OUTREACH_ACTIVE", "READY_FOR_OUTREACH", "NURTURE"], "RESPONSE_RECEIVED"),
    "escalate":              (["QUALIFIED", "CONTACT_IDENTIFIED", "READY_FOR_OUTREACH", "OUTREACH_ACTIVE",
                               "RESPONSE_RECEIVED", "CONVERSATION", "PARTNERSHIP_NEGOTIATION",
                               "EMAIL_NOT_PUBLIC", "LIVE"], "HUMAN_REVIEW"),
    "open_conversation":     (["RESPONSE_RECEIVED", "HUMAN_REVIEW"], "CONVERSATION"),
    "begin_negotiation":     (["CONVERSATION", "HUMAN_REVIEW"], "PARTNERSHIP_NEGOTIATION"),
    "partner_won":           (["PARTNERSHIP_NEGOTIATION", "HUMAN_REVIEW"], "PARTNER_WON"),
    "begin_activation":      (["PARTNER_WON"], "ACTIVATION"),
    "go_live":               (["ACTIVATION"], "LIVE"),
    "record_attribution":    (["LIVE", "ATTRIBUTION"], "ATTRIBUTION"),
    "reactivate":            (["ATTRIBUTION", "LIVE", "NURTURE"], "CONVERSATION"),
    "suppress":              (STATES, "SUPPRESSED"),
    "human_override":        (STATES, None),
}

# Events that only a human may fire.
HUMAN_ONLY_EVENTS = {"partner_won", "begin_negotiation", "human_override", "go_live"}

# Events whose guard must be satisfied by the caller passing gate results.
GUARDED = {
    "ready_for_outreach": "qualification_gates_passed",
    "start_outreach": "send_authorized",
}


class TransitionError(ValueError):
    pass


def allowed_events(state):
    return sorted(e for e, (froms, _) in TRANSITIONS.items() if state in froms)


def can(state, event):
    spec = TRANSITIONS.get(event)
    return bool(spec) and state in spec[0]


def apply(record, event, actor="agent", context=None, target_state=None, log=True):
    """Apply an event to a record dict. Mutates and returns the record.

    actor must be "human" for human-only events. context carries guard results.
    """
    context = context or {}
    state_before = record.get("state")
    if state_before not in STATES:
        raise TransitionError("record is in unknown state %r" % state_before)

    spec = TRANSITIONS.get(event)
    if spec is None:
        raise TransitionError("unknown event %r" % event)

    froms, to = spec
    if state_before not in froms:
        raise TransitionError(
            "cannot %s from %s; legal events here: %s"
            % (event, state_before, ", ".join(allowed_events(state_before)))
        )

    if state_before in TERMINAL and event != "human_override":
        raise TransitionError("%s is terminal; only a human may move it" % state_before)

    if event in HUMAN_ONLY_EVENTS and actor != "human":
        raise TransitionError("%s requires actor='human'" % event)

    if event in GUARDED and not context.get(GUARDED[event]):
        raise TransitionError("%s blocked: %s is not satisfied" % (event, GUARDED[event]))

    if event == "human_override":
        if target_state not in STATES:
            raise TransitionError("human_override needs a valid target_state")
        to = target_state

    record["state"] = to
    history = record.setdefault("state_history", [])
    history.append({
        "at": audit.now(),
        "event": event,
        "from": state_before,
        "to": to,
        "actor": actor,
        "reason": context.get("reason"),
    })
    if log:
        audit.record(
            action="state_transition",
            agent=context.get("agent", "orchestrator"),
            organization=record.get("organization_id"),
            input={"event": event, "actor": actor},
            decision=context.get("reason"),
            state_before=state_before,
            state_after=to,
            human_override=(event == "human_override"),
        )
    return record


def outreach_permitted(record, policy_path=None):
    """Whether the current autonomy level allows sending for this record.

    Tier A is human-approved at every level. Level 3 permits Tier 2 categories a
    human listed in policy. Anything else is draft-only.
    """
    level = policy.autonomy_level(path=policy_path)
    tier = record.get("partner_tier")
    band = record.get("priority_band")

    if tier == "A" or band == "STRATEGIC":
        return False, "tier A / strategic organizations are always human-approved"
    if level < 3:
        return False, "autonomy level %d is draft-only" % level
    approved = policy.get("autonomy.autonomous_send_enabled_categories", [], path=policy_path)
    org_type = record.get("organization_type")
    if level == 3:
        if band != "TIER_2":
            return False, "level 3 permits automated outreach for TIER_2 only"
        if org_type not in approved:
            return False, "category %r is not in autonomous_send_enabled_categories" % org_type
        return True, "level 3, TIER_2, approved category"
    if org_type not in approved:
        return False, "category %r is not in autonomous_send_enabled_categories" % org_type
    return True, "level %d, approved category" % level
