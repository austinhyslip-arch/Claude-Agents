---
description: The full autonomous loop, from discovery through compliance validation. Stops at human review. Never sends.
argument-hint: <category> [count]  e.g. chambers 100
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch, mcp__Clay__find-and-enrich-company, mcp__Clay__query-objects, mcp__Clay__ask-question-about-accounts, mcp__Attio__search-records, mcp__Attio__list-records
---

Run the full loop for: $ARGUMENTS

Order: discovery, deduplication, research, scoring, qualification, contact discovery, opportunity identification, signal detection, outreach preparation, compliance validation. Then stop.

Read `chanty-ecosystem-agent/CLAUDE.md` first. Follow the workflows in `chanty-ecosystem-agent/workflows/`.

Hard stops built into this command:
- No enrichment providers, ever, for contact data. Ask me instead.
- No guessed emails. `EMAIL_NOT_PUBLIC` and ask me.
- No sending. The posture is draft, don't send, and autonomy is level 0.
- Strategic and Tier A organizations always come to me, whatever the autonomy level says.

Finish with the run report:

    NEW / QUALIFIED / TIER 1 / TIER 2 / NURTURE / PUBLIC CONTACTS /
    EMAIL_NOT_PUBLIC / SIGNALS / DRAFTS / HUMAN REVIEW / ENRICHMENT USED

ENRICHMENT USED must read 0. If it would not, you have made a mistake, so stop and tell me.
