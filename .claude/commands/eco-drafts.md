---
description: Write outreach drafts and run them through the claims and personalization gates. Sends nothing.
argument-hint: <tier1|tier2|ORG-ID>
allowed-tools: Bash, Read, Glob, Grep, WebFetch
---

Draft outreach for: $ARGUMENTS

Read `chanty-ecosystem-agent/agents/outreach.md` and `chanty-ecosystem-agent/config/offers.md`.

Structure: relevance, observation, value, fit, CTA. Short. Human. No flattery, no invented urgency, no statistics we do not have. Every specific claim about the organization goes in `personalization_claims` with its source URL and type.

Then:

    cd chanty-ecosystem-agent/scripts && python3 -m eco draft-check '<json>'

Show me, per draft: organization, contact and title, the evidence behind each personalized line, the trigger, the offer, the draft itself, and your confidence. Then stop. Do not send.
