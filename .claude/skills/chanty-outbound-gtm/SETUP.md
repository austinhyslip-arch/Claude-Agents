# Setup and operating notes

What has to be true before this agent can run, and what is still missing. Last checked
2026-09-02.

## How the agent gets invoked

- **On-demand**: ask for it in any session where this repo is checked out. "Build this
  week's healthcare list", "draft today's outbound", "sweep the replies".
- **Scheduled**: no Routine exists yet. Three would be needed:

| Mode | Suggested schedule | Central | Cron (UTC, while CDT) |
|---|---|---|---|
| List build | Monday morning | 07:00 Mon | `0 12 * * 1` |
| Draft run | Weekday mornings | 07:00 Mon to Fri | `0 12 * * 1-5` |
| Reply sweep | Weekday afternoons | 16:30 Mon to Fri | `30 21 * * 1-5` |

Claude Code Routines take UTC cron only, so those expressions shift by an hour when Central
returns to CST on **Nov 1, 2026** (add one to the hour) and shift back on **Mar 14, 2027**.
Same trap the competitive intel skill documents.

## Dependencies

| Dependency | Status | Notes |
|---|---|---|
| Skill stack | **Installed and committed** | 21 skills vendored into `.claude/skills/`, recorded in `skills-lock.json` at the repo root. Copied rather than symlinked, so a fresh clone has them. |
| Attio | **Connected** | Workspace `Chanty`, admin as austin@chanty.com. Stock schema, no custom fields, no Deals object. See `.claude/gtm/attio-schema.md` for how the agent works around that. |
| Apollo | **Connected** | 135 lead credits, cycle ends 2026-09-16. Direct dials already at zero. Export credits zero. Approval still required before any spend. |
| Clay | **Connected** | Workspace `Chanty` (1356452). Reserved for the Personal list. |
| Hunter | **Not connected** | The middle rung of the waterfall. Without it the sequence is Apollo then Clay, and there is no independent verification step. |
| Gmail | Connected | Reading replies and staging drafts only. |
| Google Calendar | Connected | Checking real availability before a specific time goes into an email, which the CTA rule needs. |
| Attio native Gmail sync | **Unverified** | The CRM rules assume it catches Austin's sent mail. Confirm with one real send before relying on it. |
| Calendly to Attio via Zapier | **Unverified** | If the Zap is not live, booked meetings need manual confirmation. Check before the first one gets booked. |
| Web search and page fetch | **Restricted in this container** | Direct fetches to `google.com` and the provider APIs are refused by the network egress policy here. npm and GitHub are reachable, which is how the skills installed. Free-web-search sourcing is the entire first step, so real list building needs a session with open egress or the connectors doing the fetching. |

## The one place the brief and the skills disagreed

The brief had `outbound-triggers-6` ranking buying signals like leadership changes and
hiring. The installed skill does something else. It holds six entry premises for cold
accounts (CXO Passdown, Groundswell, Multi-Persona, plain cold). The signal ranking the
brief described is `buying-signals-6`, with the wider catalogue in the five `bridgebound-*`
skills.

Those six extra skills were installed on top of the fifteen the brief named, since the
ranking step had nothing to run on otherwise. Both jobs now happen, at different steps.

## Still blocked on Austin

1. **Chanty closed-won data.** Recalibrates the provisional buying power thresholds in
   `references/lists-and-icp.md` and feeds `icp-lookalike-expansion`. Every non-healthcare
   vertical is paused until it arrives. Useful shape: company name, size, industry, how they
   were sourced, what they replaced, who signed, how long the cycle took.
2. **Attio custom fields.** Option A in `.claude/gtm/attio-schema.md` runs today with notes
   and lists. Option B is cleaner and sortable, but the MCP connection cannot create
   attributes, so those need adding in the Attio UI. Worth doing before the first real list
   build if there is time.
3. **Follow-up cadence.** The brief covers first touches only. The agent stages first
   touches and nothing else until a sequence is defined.
4. **Hunter, if it is wanted.** Optional. Apollo and Clay both return their own verification,
   it is just not independent.

## Adding more skills later

From the repo root:

```
npx skills add swan-gtm/gtm-skills -s "<skill-name>" -a claude-code --copy -y
```

One `-s` flag per skill, since a comma-separated list silently matches nothing. `--copy`
matters, because the default symlinks into `node_modules` and those break in a fresh
container. Run it from the repo root or it writes a nested `.claude/skills` inside wherever
you are. Commit what it writes, including `skills-lock.json`.

## State and git

`state/run-log.md`, `state/send-queue.md`, `state/open-approvals.md` and
`state/credit-log.md` are the agent's memory. They only work if each run commits them. A run
that stages twenty emails and leaves the queue uncommitted will re-source and re-draft the
same people next time.

## The three locks, restated

1. **No auto-send.** The agent stages, Austin sends. That covers Apollo's sender too, which
   is why its emailer and sequence tools are banned in `.claude/gtm/sourcing-and-credits.md`.
2. **No unapproved credit spend.** Free search first, gaps batched, one question, then wait.
3. **No inferred stage advancement.** Past `Meeting Booked`, a human confirms.
