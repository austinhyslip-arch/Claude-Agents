---
description: Write outreach drafts, gate them, and put them in Austin's Gmail drafts. Sends nothing.
argument-hint: <tier1|tier2|ORG-ID>
allowed-tools: Bash, Read, Glob, Grep, WebFetch, mcp__Gmail__create_draft
---

Draft outreach for: $ARGUMENTS

Read `chanty-ecosystem-agent/agents/outreach.md` and `chanty-ecosystem-agent/config/offers.md`.

Structure: relevance, observation, value, fit, CTA. Short. Human. No flattery, no invented urgency, no statistics we do not have. Every specific claim about the organization goes in `personalization_claims` with its source URL and type.

If the offer is a workshop or an event slot, say in the first message that we would join remotely rather than in person. We do not travel, and they should know that while they are deciding rather than after. Written resources need no such line.

Format rules, no exceptions:
- Plain text only. No bold, no bullets, no numbered lists, no headings, no markdown, no HTML.
- No sign-off. No "Best", no "Thanks", no name, no title, no links block. The message ends on its last real sentence. Gmail's native signature handles the rest.

Then:

    cd chanty-ecosystem-agent/scripts && python3 -m eco draft-check '<json>'
    cd chanty-ecosystem-agent/scripts && python3 -m eco gmail-draft '<json>'

`gmail-draft` runs the format, claims and personalization gates, refuses any contact without a public email, and prints the `mcp__Gmail__create_draft` call. Make that call so the draft lands in Gmail. Pass `body` only, never `htmlBody`.

Then show me, per draft: organization, contact and title, the evidence behind each personalized line, the trigger, the offer, the draft itself, and your confidence. Then stop. I send them.
