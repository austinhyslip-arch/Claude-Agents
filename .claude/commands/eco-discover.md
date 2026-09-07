---
description: Discover organizations that could distribute Chanty to SMBs. Verifies, dedupes, saves. Contacts nobody.
argument-hint: <category> [count]  e.g. chambers 100
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch, mcp__Clay__find-and-enrich-company, mcp__Clay__query-objects, mcp__Clay__ask-question-about-accounts
---

Run the discovery workflow for: $ARGUMENTS

Read `chanty-ecosystem-agent/agents/discovery.md` and `chanty-ecosystem-agent/workflows/discovery.md` first, then follow them.

Rules that apply no matter what the arguments say:
- Public web research only. Clay company tools are fine. Apollo, ZoomInfo and Clay contact tools are blocked; run `python3 -m eco check-tool <name>` from `chanty-ecosystem-agent/scripts` if unsure.
- Verify every organization on its own website before creating a record.
- Two pieces of A or B evidence minimum, with URLs and dates.
- `python3 -m eco dedupe-check` before `python3 -m eco add-org`.
- Do not contact anyone. Do not find contacts. That is a different command.

Report: found, verified, duplicates skipped, created, empty categories.
