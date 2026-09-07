---
description: Find recent, dated, legitimate reasons to contact qualified organizations.
argument-hint: <tier1|tier2|ORG-ID>
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch
---

Find signals for: $ARGUMENTS

Read `chanty-ecosystem-agent/agents/signal.md`.

Each signal needs: what it is, the date of the thing itself, source URL and type, why it makes Chanty relevant to this audience, confidence, and a recommended action. If you cannot write the relevance sentence, it is news, not a signal, and it does not get recorded.

    cd chanty-ecosystem-agent/scripts && python3 -m eco add-signal '<json>'

Decay bands are computed from the date. Never manufacture urgency.
