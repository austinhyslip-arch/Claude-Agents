# Setup and operating notes

## How the agent gets invoked

On demand only. Austin pastes contacts into any session where this repo is checked out and
asks for outreach. There is no Routine, no schedule, and no cadence automation. That is the
design, not a gap.

## Before the first real run

The People object is set up and no manual step is outstanding. Two tracking fields exist:

- `stage`, Attio's **status** type, eleven options from Not Contacted through Follow Up
  Needed. Exact titles and their casing quirks are in `references/attio-logging.md`.
- `who_contacted`, **text**, with a three-value convention this agent must follow exactly.

Two notes on what is there:

1. `who_contacted` being free text means nothing enforces the convention. Converting it to
   a single Select with the same three values would make drift impossible. Worth doing
   before the record count grows.
2. `Follow Up Needed` sits at order 11, after the closed stages. That is fine if it is a
   queue flag, which is how the agent treats it. If it is meant as a pipeline position it
   should be reordered to sit near Follow-Up Sent.

**Run mail-tester** before the first real batch from the sending address.

## Dependencies at run time

Verified September 2, 2026 in the remote environment.

| Dependency | Status | Notes |
|---|---|---|
| Attio | **Connected and set up.** Workspace `Chanty`, austin@chanty.com, admin. | Objects are `people` and `companies` only. Pipeline tracking lives on `people` via `stage` and `who_contacted`. Still no Deals object, so one person carries one stage, which caps things at one open opportunity per human. One list exists, `customer_success` on companies, which this agent never writes to. Write path is documented but not yet exercised against a real record. |
| Apollo | **Connected.** 135 lead credits, 0 used, cycle Sept 2 to **Sept 16**. | Two-week cycle, not monthly. Export credits 0 and direct dial 0, so no exports and no phone lookups. Carries email reveal and verification now that Hunter is out. Credit-gated. |
| Clay | **Connected.** Workspace `Chanty` (1356452). | Last in the waterfall. Roughly 100 data credits a month. Credit-gated. |
| Gmail | Connected and enabled. | Drafts only, on request. This agent never calls a send tool in its normal flow. |
| Google Calendar | Connected. | Not used directly. Bookings from the Meet link show up on the Attio record as `next_calendar_interaction`, which is how Meeting Booked gets set. |
| Hunter.io | **Not connected, and not in the connector directory.** | No longer needed. Apollo covers verification. Remove it from the stack list. |
| Calendly | **Dropped from the stack.** | Replaced by the Google Meet booking link, https://calendar.app.google/S56CDe5cBYwNanz39. Nothing automated writes Meeting Booked now, so the agent owns that stage. |
| Zapier | **No longer needed by this agent.** | It existed to push Calendly bookings into Attio. With Calendly gone there is nothing for it to do here. |
| Web search | Available. | Primary free research tool. |
| Direct page fetch | Unreliable in this environment. | The competitive intel agent had fetches to common domains refused by the network egress policy. Expect the same on LinkedIn and some company sites. Fall back to search snippets and mark the angle unverified. |
| `personalization-playbooks`, `persona-mapping-framework`, `cold-email-strategist` | Not installed. | `references/` carries a standalone version of each. If they get installed, the installed version wins. |
| Mailtrack | Browser extension, not a connection. | Never treat an open as a stage change. See `references/attio-logging.md`. |
| RB2B, Google Alerts, Google Postmaster, mail-tester | Out of scope. | Sourcing and deliverability infrastructure, owned elsewhere. |

## Sending limits

Free Gmail is safe at roughly 20 to 30 a day against a 500 hard cap. The agent warns at
about 25 in a day.

## Apollo tools this agent must not touch

`apollo_emailer_*` and `apollo_sequences_*` are cadence automation, which is out of scope,
and `apollo_emailer_messages_send_now` would break the no-send rule outright. Enrichment
and match tools only.

## Open items

1. **Chanty customer win data.** Still pending. Unlocks non-healthcare proof points, which
   is what the middle of most of these drafts is missing.
2. **`who_contacted` is free text.** Convention documented, nothing enforcing it. A Select
   would.
3. **"Follow Up Needed" semantics.** Treated as a queue flag, inferred from the name and its
   position. Confirm that is what Austin meant.
4. **Attio native Gmail sync.** Unconfirmed. `references/attio-logging.md` handles it by
   searching the record for an already-synced copy before attaching a note. Confirm it once
   and that check can be simplified.
5. **Multi-touch cadence ownership.** Unresolved whether `cold-email-strategist` covers full
   cadence architecture. Out of scope for this agent either way, it drafts one message at a
   time, but it becomes a real gap once volume rises.
6. **Agent 1 does not exist in this repo.** The spec names its copywriting pipeline order and
   its dedup logic as the source of truth. Neither is available, so both were written
   standalone here. When Agent 1 lands, reconcile the two rather than letting them drift,
   and make sure both write `stage` and `who_contacted` the same way. Two agents writing one
   pipeline field with different rules is worse than no pipeline field.

## State and git

`state/send-log.md` is the agent's memory of what went out. It only works if the run that
logs a send also commits it.
