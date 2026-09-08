---
description: Run the full send gate on drafts. Blocks anything that fails. Never sends; Austin sends from Gmail.
argument-hint: <OUT-ID|approved>
allowed-tools: Bash, Read, Glob, Grep
---

Run the send gate on: $ARGUMENTS

    cd chanty-ecosystem-agent/scripts && python3 -m eco send-check '<draft json>'

A record only qualifies if it passed every hard qualification gate, the factuality gate, format, suppression, the contact data policy, has a publicly found email, uses approved messaging, and needs no escalation.

At autonomy level 2 this will pass everything except `autonomy_or_human_approval`. That is correct. Drafts go to my Gmail and I send them.

If anything else fails: show me the named failures and stop.

Automated outreach turns on only after I have read the first 20 drafts and told you to turn it on. Do not raise the autonomy level yourself, and do not ask me to raise it before those 20 exist and I have read them.
