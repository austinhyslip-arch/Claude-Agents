# Chanty GTM Agent System

Two agents share one set of rules. This directory holds the rules. Each agent keeps its own
workflow and state inside its own skill folder, but neither agent gets to invent its own
version of how credits are spent, how email is written, or how Attio is updated.

## Agents

| Agent | Skill | Status |
|---|---|---|
| 1. Outbound GTM Agent | `.claude/skills/chanty-outbound-gtm/` | Built. Healthcare ready to run, other industries blocked on win data. |
| 2. (not yet specified) | not created | Waiting on the spec from Austin. |

Agent 2 was named in the original brief but its section was never written down. Nothing in
this repo assumes what it does. When the spec lands, it gets its own skill folder next to
Agent 1 and reads the same four contracts below.

## Shared contracts

Both agents read these before acting. If one of them conflicts with an agent's own
reference file, the contract wins.

- `sourcing-and-credits.md`: free search first, batch the gaps, never spend a credit
  without approval
- `copywriting.md`: the pipeline order and the send-performance rules that override it
- `attio-schema.md`: the objects, fields and views the agents read and write
- `crm-sync.md`: what updates automatically, what gets flagged, what never moves on its own

## Skill stack

Installed with `npx skills add swan-gtm/gtm-skills`. See the agent's `SETUP.md` for the
install check.

| Skill | Used for |
|---|---|
| `research` | company, contact and signal lookups underneath everything else |
| `build-list` | ICP criteria into a scored contact list |
| `icp-lookalike-expansion` | widening the list off closed-won data |
| `never-guess-an-email` | verification before send |
| `outbound-triggers-6` | ranking the buying signal behind an account |
| `outreach-4-categories` | Inbound / Postbound / Bridgebound / Outbound |
| `bridge-before-cold` | is there a warm path before we go cold |
| `persona-mapping-framework` | mapping the buying committee |
| `personalization-playbooks` | picking the angle per contact |
| `b2b-cold-email-copywriting` | core email structure |
| `cold-email-strategist` | first-touch strategy |
| `josh-braun-copywriting` | hook and psychology |
| `frontal-messaging-templates` | structure and deliverability reference only |
| `human-mannerisms` | final pass to strip AI-sounding language |
| `handle-reply` | classifying inbound replies and drafting the next action |

If a skill in this list is not installed, say so in the run summary and fall back to the
agent's own reference file. Do not quietly skip a step in the pipeline.
