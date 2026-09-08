"""Gmail draft planning.

Drafts land in Austin's Gmail. He reads each one and sends it himself. Nothing
here sends, and nothing here can: this module builds the payload for
`mcp__Gmail__create_draft` and the agent makes the call after the gates pass.

Two things are enforced at the payload level rather than left to a reminder:
`htmlBody` is never set, so Gmail treats the message as plain text, and the body
is checked for markdown, HTML and sign-offs before a payload is produced at all.
Gmail supplies the signature and the formatting.
"""

from . import gates, policy


class DraftRejected(ValueError):
    def __init__(self, gate_results):
        self.gate_results = gate_results
        names = []
        for result in gate_results:
            names.extend(c["check"] for c in result.failures)
        super().__init__("draft rejected: %s" % ", ".join(names))


def build(draft, contact, policy_path=None):
    """Return the create_draft arguments, or raise with the failing checks.

    The contact must carry a publicly found email. A contact in any other state
    has no business reaching a mailbox.
    """
    if contact.get("email_status") != "public_verified":
        raise DraftRejected([_single("contact_email_public", False,
                                     "email_status=%r" % contact.get("email_status"))])

    body = draft.get("body") or ""
    subject = draft.get("subject") or ""

    checks = [
        gates.check_format(body, policy_path=policy_path),
        gates.check_claims("\n".join([subject, body]), policy_path=policy_path),
        gates.check_personalization("\n".join([subject, body]),
                                    draft.get("personalization_claims")),
    ]
    failed = [c for c in checks if not c.passed]
    if failed:
        raise DraftRejected(failed)

    if not subject.strip():
        raise DraftRejected([_single("subject_present", False, "subject is empty")])

    return {
        "to": [contact["email"]],
        "subject": subject.strip(),
        "body": body.rstrip() + "\n",
        # htmlBody is deliberately absent. Setting it would make Gmail send a
        # rich-text alternative and undo the plain-text rule.
    }


def _single(name, passed, detail):
    g = gates.GateResult("gmail_draft")
    g.add(name, passed, detail)
    return g


def plan(draft, contact, organization=None, policy_path=None):
    """The call to make, plus the context a reviewer needs in the Gmail list."""
    args = build(draft, contact, policy_path=policy_path)
    return {
        "tool": "mcp__Gmail__create_draft",
        "args": args,
        "review_context": {
            "organization": (organization or {}).get("organization_name"),
            "organization_id": draft.get("organization_id"),
            "contact": contact.get("full_name"),
            "title": contact.get("title"),
            "email_source": contact.get("email_source_url"),
            "offer": draft.get("offer"),
            "touch_number": draft.get("touch_number"),
            "evidence": [
                {"claim": e.get("claim"), "source_url": e.get("source_url"),
                 "source_type": e.get("source_type")}
                for e in (draft.get("personalization_claims") or [])
            ],
        },
        "sending_mode": policy.get("email_compliance.sending_mode", path=policy_path),
        "note": "Creates a draft only. Austin reads it and sends it. "
                "No signature and no formatting are added here; Gmail does both.",
    }
