# Setup and operating notes

Agent 2 of the Chanty GTM system. Shared setup, connector state and credit balances live in
`.claude/gtm/README.md` and `.claude/gtm/sourcing-and-credits.md`. This file covers only
what is specific to drafting on demand.

## How it gets invoked

On demand only. Austin pastes contacts into any session where this repo is checked out and
asks for outreach. No Routine, no schedule, no cadence automation. That is the design, not
a gap.

Agent 1 runs on its own cadence and has its own run modes. The two do not coordinate through
anything except the Attio record and the `who_contacted` field on it.

## What is different from Agent 1

| | Agent 1 | Agent 2 |
|---|---|---|
| Trigger | Its own cadence | Austin asks |
| Targets | Sourced and scored | Handed over in the conversation |
| Output | Staged in `state/send-queue.md` | Handed back in the conversation, optionally a Gmail draft |
| Sending | Austin works the queue | Austin sends from Gmail |
| `who_contacted` | `Agent 1 (automated)` | `Austin (manual)` |
| Approvals | `state/open-approvals.md` | Answered in the conversation, filed only if left unresolved |
| Send window, pacing, daily cap | Enforced | Not applicable, except the roughly 25 a day Gmail warning |

## Before the first real run

Nothing is outstanding on this agent's side. Two things are worth doing before volume, both
covered in `.claude/gtm/attio-schema.md`:

1. **`who_contacted` is free text.** A single Select with the three agreed values would make
   drift impossible, and it is far cheaper now than after the table fills.
2. **`Do Not Contact` and `Bounced` are not options on the `stage` field.** Both are required
   by `crm-sync.md`. The interim writes them into the `GTM record` note, which works but
   makes an opt-out discoverable only by reading a note body. Adding the two options is the
   real fix.

**Run mail-tester** before the first real batch from the sending address.

## Known gaps

1. **Chanty customer win data.** Still the biggest one, and shared with Agent 1. Without it
   the middle of a cold email has no proof point outside healthcare, and
   `icp-lookalike-expansion` and the buying power thresholds stay blocked.
2. **The write path is unexercised.** Nothing has been written to Attio by either agent yet.
   The schema is read from the live workspace so the field names are right, but the first
   real record is where the `personal_name` "Last, First" format, the `stage` status write
   and the company dual write get proven.
3. **Attio native Gmail sync.** Unconfirmed. Step 6 searches for an already-synced copy
   before writing a note, so a duplicate is avoided either way, but confirming it once would
   simplify the check.
4. **No Deals object.** One person carries one stage, so one open opportunity per human.
   Fine now, and much cheaper to fix before the data is in than after.

## State and git

`state/send-log.md`, `state/credit-log.md` and `state/open-approvals.md` are this agent's
memory. They only work if the run that writes them also commits them.
