# Setup and operating notes

## How the agent gets invoked

On demand only. Austin pastes contacts into any session where this repo is checked out and
asks for outreach. There is no Routine, no schedule, and no cadence automation. That is the
design, not a gap.

## Dependencies at run time

Checked September 2, 2026 in the remote environment.

| Dependency | Status | Notes |
|---|---|---|
| Attio | **Not connected** | Exists in the connector directory (Search, manage and update your Attio CRM) but is not installed. Until it is, dedup and logging cannot run. The agent still drafts, and `state/send-log.md` holds the record. Connect at claude.ai, then confirm the tools load in the session. |
| Gmail | Connected and enabled | Used for drafts only, on request. This agent never calls a send tool as part of its normal flow. |
| Apollo.io | **Not connected** | In the directory, not installed. Credit-gated once it is. |
| Hunter.io | **Not in the connector directory** | No connector turned up under that name. Either use it in the browser and paste the result back, or find another verification path. Verification is the one gap that actually blocks a send, so it is worth solving. |
| Clay | **Not connected** | In the directory, not installed. Last in the waterfall anyway. |
| Calendly | **Not connected** | In the directory, not installed. Only matters for the Meeting Booked stage rule. |
| Web search | Available | Primary free research tool. |
| Direct page fetch | Unreliable in this environment | The competitive intel agent had fetches to common domains refused by the network egress policy. Expect the same on LinkedIn and some company sites. Fall back to search snippets and mark the angle unverified. |
| `personalization-playbooks`, `persona-mapping-framework`, `cold-email-strategist` | Not installed | `references/` carries a standalone version of each. If they get installed, the installed version wins. |
| Mailtrack | Browser extension | Not a connection. Never treat an open as a stage change, see `references/attio-logging.md`. |
| Zapier, RB2B, Google Alerts, Google Postmaster, mail-tester | Out of scope here | Sourcing and deliverability infrastructure. Only the Calendly to Attio Zap touches this agent, through the Meeting Booked rule. |

## Sending limits

Free Gmail is safe at roughly 20 to 30 a day against a 500 hard cap. The agent warns at
about 25 in a day. Run mail-tester before the first real batch from any new address.

## Open items

Carried over from the spec, plus what this build surfaced.

1. **Chanty customer win data.** Still pending. Unlocks non-healthcare proof points, which
   is what the middle of most of these drafts is missing.
2. **Multi-touch cadence ownership.** Unresolved whether `cold-email-strategist` covers
   full cadence architecture. Out of scope for this agent either way, it drafts one message
   at a time, but it becomes a real gap once volume rises.
3. **Attio native Gmail sync.** Unconfirmed. `references/attio-logging.md` handles it by
   checking the record for an already-synced copy before attaching a note. Confirm it once
   and that check can be simplified.
4. **Calendly to Attio Zapier.** Unconfirmed. Until it is, the agent leaves Meeting Booked
   alone rather than risking a double write.
5. **What the Personal list actually is.** Buyer outreach, career and network outreach, or
   both. `references/persona-map.md` covers both and should be trimmed once this is
   settled.
6. **Agent 1 does not exist in this repo.** The spec references its copywriting pipeline
   order and its dedup logic as the source of truth. Neither is available, so both were
   written standalone here. When Agent 1 lands, reconcile the two rather than letting them
   drift.

## State and git

`state/send-log.md` is the agent's memory of what went out. It only works if the run that
logs a send also commits it.
