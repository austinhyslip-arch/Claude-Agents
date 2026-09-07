---
description: Run the full send gate on approved drafts. Blocks anything that fails. Sends nothing without explicit approval.
argument-hint: <OUT-ID|approved>
allowed-tools: Bash, Read, Glob, Grep
---

Run the send gate on: $ARGUMENTS

    cd chanty-ecosystem-agent/scripts && python3 -m eco send-check '<draft json>'

A record only qualifies if it passed every hard qualification gate, the factuality gate, suppression, the contact data policy, has a publicly found email, uses approved messaging, and needs no escalation.

Right now this will fail on `email_compliance` (physical address, sending infrastructure and legal review are unset in policy) and on `autonomy_or_human_approval` (level 0). That is the system working as designed, not a bug.

If anything fails: do not send, show me the named failures, and stop.

If everything passes: show me exactly what would go out, to whom, and wait for my explicit go-ahead. You do not have sending infrastructure configured, so the send itself is mine to make.
