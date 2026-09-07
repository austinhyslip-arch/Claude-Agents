---
description: Research and score existing organizations. Produces evidence, scores, opportunity and qualification. No outreach.
argument-hint: <tier1|tier2|ORG-ID|all>
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch, mcp__Clay__find-and-enrich-company, mcp__Clay__ask-question-about-accounts
---

Research: $ARGUMENTS

Read `chanty-ecosystem-agent/agents/intelligence.md` and `chanty-ecosystem-agent/agents/opportunity.md`, then follow `chanty-ecosystem-agent/workflows/qualification.md`.

For each organization: audience, distribution, partnership behaviour, timing, contradictions. Score every component you researched and leave the rest null. Null scores zero, which is the point.

Then `python3 -m eco score` and `python3 -m eco gate`.

Return per organization: score and breakdown, evidence with URLs, audience with its confidence label, distribution mechanisms, recommended offer and why, recommended contact role, triggers, risks, unknowns.

No outreach. No contact discovery.
