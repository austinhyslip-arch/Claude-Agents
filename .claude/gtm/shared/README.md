# Shared data, Agent 1 to Agent 2

Agent 2 is built somewhere outside this repo, so it cannot be handed anything directly. Two
surfaces carry the data instead, and they work in that order.

## 1. Attio, the real one

Attio is the system of record for both agents. Everything from a run lands there first:
company records, person records, the `GTM account` note on each company, and the list
membership that says Personal or Agent. Agent 2 reads the same workspace, so a contact
sourced here is a contact it already has.

Workspace `Chanty`. Routing lists created 2026-09-02:

| List | api_slug | list_id |
|---|---|---|
| Healthcare / CT / Personal | `healthcare_ct_personal` | 54d05801-0490-4976-95aa-12c923494ed7 |
| Healthcare / CT / Agent | `healthcare_ct_agent` | ec286089-7d94-4d73-838a-07a585f15b7e |

Every company in those lists carries a `GTM account` note with the score, the signal, the
routing and the account state. That note is the interchange format until the custom fields
exist. Parse it, do not guess at it.

## 2. `handoff.json`, for anything Attio cannot hold

A per-run export of what Agent 1 did, in one file Agent 2 can read without an Attio call.
It carries the score components, the hold reasons and the drafts, which have nowhere natural
to live in a CRM. It is written at the end of every run and it is a snapshot, not a queue.
Attio wins on any disagreement.

## Rules for both sides

- **Attio is the source of truth.** If this file and Attio disagree, Attio is right and this
  file is stale.
- **Neither agent sends on the other's behalf.** A draft in here is a draft.
- **Do not double-touch.** Check the company's last-touched date before contacting anyone at
  an account the other agent has already worked. The dual write in `crm-sync.md` exists so
  that check is one read rather than a sweep of every person record.
- **Do not overwrite the other agent's fields.** Add a note and flag it instead.

## Open question

Where Agent 2 actually reads from has not been confirmed. If it has Attio access, it already
has everything and this file is a convenience. If it does not, it needs either this repo or
a copy of `handoff.json` pushed somewhere it can see. Ask Austin before assuming.
