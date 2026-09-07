---
description: Show the human review queue, highest leverage first, in briefs readable in under a minute.
argument-hint: [red|yellow|green|all]
allowed-tools: Bash, Read, Glob, Grep
---

Show the review queue: $ARGUMENTS

Read `chanty-ecosystem-agent/config/escalation.md` for the brief format.

Order: RED first (highest leverage, or blocked on a decision only I can make), then YELLOW, then GREEN.

Each brief: organization, contact, title, why they matter, audience, distribution channels, audience estimate with its confidence label, trigger, recommended offer, evidence, what was sent, their response, likely objective, potential seats, risks, unknown information, recommended next step.

List the unknowns as unknowns. A brief that hides what we do not know is worse than no brief.
