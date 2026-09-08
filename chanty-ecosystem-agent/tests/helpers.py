"""Shared fixtures.

Every organization and person in this directory is invented for testing and
lives only in a temp directory. None of it is a real organization, and none of
it is ever written into data/.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from eco import audit  # noqa: E402


def temp_root():
    d = tempfile.mkdtemp(prefix="eco-test-")
    for c in ("organizations", "contacts", "opportunities", "signals", "partners",
              "outreach", "attribution", "suppression", "executions"):
        os.makedirs(os.path.join(d, c), exist_ok=True)
    return d


def silence_audit(testcase):
    """Send audit writes to a temp file so tests never touch logs/audit.jsonl."""
    original = audit.record
    tmp = tempfile.mkstemp(prefix="eco-audit-")[1]

    def patched(*args, **kwargs):
        kwargs["log_path"] = tmp
        return original(*args, **kwargs)

    audit.record = patched
    testcase.addCleanup(lambda: setattr(audit, "record", original))
    return tmp


ORG = {
    "organization_id": "ORG-TESTAA01",
    "organization_name": "Example Valley Chamber of Commerce",
    "organization_type": "Chamber",
    "taxonomy_group": "smb_ecosystem",
    "website": "https://example-valley-chamber.test",
    "domain": "example-valley-chamber.test",
    "city": "Example Valley",
    "state_region": "KS",
    "country": "US",
    "national_or_local": "local",
    "status": "active",
    "audience_description": "Member businesses in the Example Valley area, mostly under 50 employees",
    "audience_size": 900,
    "audience_size_type": "members",
    "audience_confidence": "KNOWN_FACT",
    "industries": ["retail", "home services"],
    "smb_fit": "high",
    "communication_intensity": "medium",
    "distribution": {
        "newsletter": {"present": True, "confidence": "KNOWN_FACT",
                       "detail": "weekly member newsletter",
                       "source_url": "https://example-valley-chamber.test/news"},
        "events": {"present": True, "confidence": "KNOWN_FACT", "detail": "monthly luncheon",
                   "source_url": "https://example-valley-chamber.test/events"},
    },
    "evidence": [
        {"claim": "runs a weekly member newsletter", "source": "chamber website",
         "source_type": "A", "source_url": "https://example-valley-chamber.test/news",
         "date_checked": "2026-09-01", "confidence": "KNOWN_FACT"},
        {"claim": "hosts a monthly member luncheon", "source": "chamber website",
         "source_type": "A", "source_url": "https://example-valley-chamber.test/events",
         "date_checked": "2026-09-01", "confidence": "KNOWN_FACT"},
    ],
    "contradictions": [],
    "priority_band": "TIER_2",
    "partner_tier": "C",
    "state": "CONTACT_IDENTIFIED",
    "state_history": [],
    "trials": 0, "paid_accounts": 0, "seats": 0, "mrr": 0, "arr": 0, "assisted_revenue": 0,
    "created_at": "2026-09-01T00:00:00+00:00",
}

CONTACT = {
    "contact_id": "CON-TESTAA01",
    "organization_id": "ORG-TESTAA01",
    "full_name": "Jordan Rivera",
    "first_name": "Jordan",
    "last_name": "Rivera",
    "title": "Director of Membership",
    "role_category": "membership",
    "is_primary": True,
    "email": "jordan@example-valley-chamber.test",
    "email_status": "public_verified",
    "email_source_url": "https://example-valley-chamber.test/staff",
    "email_source_type": "A",
    "email_date_checked": "2026-09-01",
    "email_discovery_method": "staff_page",
    "sources_checked": ["https://example-valley-chamber.test/staff"],
    "alternative_contact_methods": [],
    "enrichment_used": False,
    "requires_user_permission": False,
    "response_history": [],
    "suppressed": False,
    "created_at": "2026-09-01T00:00:00+00:00",
}

OPPORTUNITY = {
    "opportunity_id": "OPP-TESTAA01",
    "organization_id": "ORG-TESTAA01",
    "organization_need": "member education content for the monthly luncheon",
    "audience_need": "member businesses coordinating growing teams over text and email",
    "distribution_mechanism": "newsletter",
    "recommended_offer": "educational_workshop",
    "why_this_offer": "they already run a monthly luncheon with an outside speaker",
    "why_now": "September luncheon slot is listed as open on their events page",
    "value_to_organization": "a session their members can use, no vendor pitch",
    "value_to_chanty": "direct access to member businesses in the ICP size range",
    "confidence": 0.7,
    "evidence": [],
    "risks": [],
    "unknowns": [],
    "escalation_required": False,
    "created_at": "2026-09-01T00:00:00+00:00",
}

DRAFT = {
    "outreach_id": "OUT-TESTAA01",
    "organization_id": "ORG-TESTAA01",
    "contact_id": "CON-TESTAA01",
    "opportunity_id": "OPP-TESTAA01",
    "touch_number": 1,
    "channel": "email",
    "offer": "educational_workshop",
    "subject": "Speaker idea for the October luncheon",
    "body": ("Hi Jordan,\n\nI saw the chamber runs a monthly member luncheon and that the "
             "October slot is open.\n\nWe put together practical sessions on team "
             "communication for growing businesses. Happy to run one for your members, "
             "no product pitch.\n\nWould that be useful?"),
    "personalization_claims": [
        {"claim": "hosts a monthly member luncheon", "source_type": "A",
         "source_url": "https://example-valley-chamber.test/events",
         "date_checked": "2026-09-01", "confidence": "KNOWN_FACT"},
    ],
    "status": "draft",
    "created_at": "2026-09-01T00:00:00+00:00",
}
