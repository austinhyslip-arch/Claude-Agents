---
description: The full loop, from discovery through drafts in Gmail. Stops at human review. Never sends.
argument-hint: <category> [count]  e.g. chambers 20
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch, mcp__Clay__find-and-enrich-company, mcp__Clay__query-objects, mcp__Clay__ask-question-about-accounts, mcp__Attio__search-records, mcp__Attio__list-records, mcp__Gmail__create_draft
---

Run the full loop for: $ARGUMENTS

Order: discovery, deduplication, research, scoring, qualification, contact discovery, opportunity identification, signal detection, draft writing, gate validation, then drafts into my Gmail. Then stop.

Read `chanty-ecosystem-agent/CLAUDE.md` first. Follow the workflows in `chanty-ecosystem-agent/workflows/`.

Hard stops built into this command:
- No enrichment providers, ever, for contact data. Ask me instead.
- No guessed emails. `EMAIL_NOT_PUBLIC` and ask me.
- No sending. Drafts land in Gmail and I send them.
- Plain text, no sign-off, no formatting. Gmail does both.
- Strategic and Tier A organizations always come to me, whatever the autonomy level says.

Finish with the run report:

    NEW / QUALIFIED / TIER 1 / TIER 2 / NURTURE / PUBLIC CONTACTS /
    EMAIL_NOT_PUBLIC / SIGNALS / GMAIL DRAFTS / HUMAN REVIEW / ENRICHMENT USED

ENRICHMENT USED must read 0. If it would not, you have made a mistake, so stop and tell me.
