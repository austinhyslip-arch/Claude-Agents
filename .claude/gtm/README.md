# Chanty GTM Agent System

Two agents share one set of rules. This directory holds the rules. Each agent keeps its own
workflow and state inside its own skill folder, but neither agent gets to invent its own
version of how credits are spent, how email is written, or how Attio is updated.

## Agents

| Agent | Skill | Status |
|---|---|---|
| List Building Agent | `.claude/skills/list-building-agent/` | Built. Layer 1, sourcing and qualification only. Stops at a spreadsheet, never touches Attio itself. |
| 1. Outbound GTM Agent | `.claude/skills/chanty-outbound-gtm/` | Built. Healthcare ready to run, other industries blocked on win data. |
| 2. On-Demand Outreach Drafting | `.claude/skills/outreach-drafting/` | Built. In this repo, and it writes the same Attio people records Agent 1 does. |

Three agents, not two independent ones. List Building Agent sources and qualifies, stopping
at a reviewable spreadsheet. Agent 1 sources and stages on its own cadence, and can also
work from a spreadsheet List Building Agent produced once Austin has resolved its flags.
Agent 2 drafts on demand for targets Austin hands it, from either a spreadsheet or a name
typed into the conversation, and he sends those by hand. All three write or read the same
Attio people records, and `who_contacted` is what tells the outbound agents apart once
something is actually sent. All three follow every contract below, so where any agent's own
references disagree with these files, these files win.

**A list-build spreadsheet is qualified, not verified.** List Building Agent's own "Needs
Paid Tool" column tracks whether a guess exists, not whether an address is send-eligible.
`sourcing-and-credits.md`'s verification bar (published, provider-verified, or previously
delivered) applies to every row before anything gets drafted, regardless of what that
column says. See the note on `references/enrichment.md` for how that gap was found and
closed.

`shared/` carries run output between them. Attio is the real handoff since both agents read
the same workspace; `shared/handoff.json` is a per-run snapshot of what a CRM holds badly,
mainly score components, hold reasons and staged drafts.

## Shared contracts

Both agents read these before acting. If one of them conflicts with an agent's own
reference file, the contract wins.

- `value-prop.md`: what any agent is allowed to claim about Chanty, and the numbers behind
  it. Ground truth for every claim in every email, page and digest.
- `sourcing-and-credits.md`: free search first, batch the gaps, never spend a credit
  without approval
- `copywriting.md`: the pipeline order and the send-performance rules that override it
- `attio-schema.md`: the objects, fields and views the agents read and write
- `crm-sync.md`: what updates automatically, what gets flagged, what never moves on its own

## Connectors

Verified live on 2026-09-02.

| Connector | State | Used for |
|---|---|---|
| Attio | Connected. Workspace `Chanty`, admin access as austin@chanty.com | System of record |
| Apollo | Connected | Paid contact lookup, first in the waterfall, approval required |
| Clay | Connected. Workspace `Chanty` (1356452) | Paid fallback, mostly the Personal list |
| Gmail | Connected | Reading replies, staging drafts. Never for agent sending |
| Google Calendar | Connected | Checking availability before a meeting time goes in an email |
| Hunter | **Not connected, and no connector exists in the directory** | The middle rung of the waterfall is missing and is not a matter of connecting it. Apollo carries verification. See `sourcing-and-credits.md` |
| Calendly | **Dropped from the stack** | Replaced by Austin's Google Meet link. The Zapier bridge it needed is no longer required. |

## Skill stack

The 21 skills this system uses are vendored into `.claude/skills/` and committed, so a
fresh clone or a new session has them without a network install step. `skills-lock.json` at
the repo root records the source and hash of each one.

To add another from the same library:

```
npx skills add swan-gtm/gtm-skills -s "<skill-name>" -a claude-code --copy -y
```

Run it from the repo root. One `-s` flag per skill, since a comma-separated list is not
matched. `--copy` matters, because the default symlinks into `node_modules` and those links
break in a fresh container. Commit what it writes.

### What each skill does here

| Skill | Used for |
|---|---|
| `research` | company, contact and signal lookups underneath everything else |
| `build-list` | ICP criteria into a scored contact list |
| `icp-lookalike-expansion` | widening the list off closed-won data |
| `never-guess-an-email` | published versus assembled addresses, role inbox ranking, suppression |
| `buying-signals-6` | ranking the buying signal behind an account |
| `bridgebound-firmographic-15` | business-event triggers: funding, M&A, growth, relocation |
| `bridgebound-in-market-20` | active-buyer triggers: adjacent vendors, competitors, timing |
| `bridgebound-symptoms-11` | pain-based triggers: complaints, gaps, influencer audiences |
| `bridgebound-history-16` | past-prospect triggers: closed-lost, old demos, churn |
| `bridgebound-relationship-39` | warm-connection triggers, feeds the bridge check |
| `outreach-4-categories` | Inbound / Postbound / Bridgebound / Outbound |
| `bridge-before-cold` | is there a warm path, and what one-line premise comes out of it |
| `outbound-triggers-6` | the entry premise for a genuinely cold account |
| `persona-mapping-framework` | mapping the buying committee |
| `personalization-playbooks` | how much personalization a category earns |
| `b2b-cold-email-copywriting` | core email structure |
| `cold-email-strategist` | first-touch strategy and deliverability |
| `josh-braun-copywriting` | hook and psychology |
| `frontal-messaging-templates` | six message structures, reference only |
| `human-mannerisms` | final pass to strip AI-sounding language |
| `handle-reply` | classifying inbound replies and drafting the next action |

**One correction against the original brief.** It had `outbound-triggers-6` ranking buying
signals like leadership changes and hiring. That is not what the skill does. It holds six
entry premises for cold accounts: CXO Passdown, two Groundswell plays, Groundswell to
decision maker, Multi-Persona, and plain cold. The signal ranking the brief described is
`buying-signals-6`, and the trigger catalogue behind it is the five `bridgebound-*` skills.
Those six were installed on top of the fifteen the brief named, because otherwise the
ranking step had nothing to run on.
