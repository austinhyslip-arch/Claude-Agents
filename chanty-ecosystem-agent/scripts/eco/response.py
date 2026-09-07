"""Response handling.

Classification is the Response Agent's job. What is deterministic, and therefore
lives here, is what a classification *means*: which ones stop automation, which
escalate, and which write suppression.
"""

from . import policy

CLASSES = ["POSITIVE", "MEETING", "PARTNERSHIP", "PROGRAMMING", "REFERRAL", "PRICING",
           "NEUTRAL", "NEGATIVE", "SUPPRESS", "WRONG_PERSON", "OOO", "AMBIGUOUS"]

# OOO is the only class that does not stop the sequence; it pauses it.
NON_STOPPING = {"OOO"}

ESCALATES = {"PRICING", "PARTNERSHIP", "MEETING", "SUPPRESS", "REFERRAL", "AMBIGUOUS"}

SUPPRESSES = {"SUPPRESS"}


def stops_automation(classification):
    if classification not in CLASSES:
        raise ValueError("unknown classification %r" % classification)
    return classification not in NON_STOPPING


def requires_human(classification, body=""):
    if classification in ESCALATES:
        return True
    lowered = (body or "").lower()
    triggers = policy.get("human_escalation_triggers", [])
    keyword_map = {
        "pricing_question": ["price", "pricing", "cost", "how much", "per seat"],
        "commission_request": ["commission", "referral fee", "cut of"],
        "referral_economics": ["rev share", "revenue share", "affiliate"],
        "contract_request": ["contract", "msa", "agreement", "terms"],
        "exclusivity_request": ["exclusive", "exclusivity"],
        "data_sharing_request": ["data sharing", "share data", "member list"],
        "security_question": ["security", "soc 2", "soc2", "penetration"],
        "compliance_question": ["compliance", "gdpr", "privacy policy"],
        "hipaa": ["hipaa", "phi", "baa"],
        "legal_issue": ["legal", "counsel", "attorney"],
        "media_request": ["press", "reporter", "journalist", "interview"],
        "complaint": ["complaint", "spam", "stop emailing", "unsolicited"],
    }
    for trigger in triggers:
        for kw in keyword_map.get(trigger, []):
            if kw in lowered:
                return True
    return False


def writes_suppression(classification, body=""):
    if classification in SUPPRESSES:
        return True
    lowered = (body or "").lower()
    return any(p in lowered for p in
               ["unsubscribe", "remove me", "take me off", "do not contact",
                "stop emailing", "no further contact"])


def plan(classification, body=""):
    """What the system does next, as data rather than prose."""
    if classification not in CLASSES:
        raise ValueError("unknown classification %r" % classification)
    return {
        "classification": classification,
        "stop_automation": stops_automation(classification),
        "escalate": requires_human(classification, body),
        "suppress": writes_suppression(classification, body),
        "next_event": _next_event(classification, body),
    }


def _next_event(classification, body):
    if writes_suppression(classification, body):
        return "suppress"
    if classification in ("POSITIVE", "MEETING", "PARTNERSHIP", "PROGRAMMING",
                          "REFERRAL", "PRICING"):
        return "escalate"
    if classification in ("NEGATIVE", "WRONG_PERSON"):
        return "nurture"
    if classification == "OOO":
        return None
    return "escalate"
