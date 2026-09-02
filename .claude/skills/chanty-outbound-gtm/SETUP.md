# Setup and operating notes

What has to be true before this agent can actually run, and what is not true yet. Written
2026-09-02.

## How the agent gets invoked

- **On-demand**: ask for it in any session where this repo is checked out. "Build this
  week's healthcare list", "draft today's outbound", "sweep the replies".
- **Scheduled**: no Routine exists yet. Three would be needed, and they are worth adding
  only once the dependencies below are green:

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
| `swan-gtm/gtm-skills` | **Not installed** | Nothing from the stack is present in this environment. Install with `npx skills add swan-gtm/gtm-skills`. Until then the agent falls back to its own reference files, which cover the rules but not the underlying skill logic. Say so in the run summary rather than pretending the pipeline ran. |
| Attio | **No connector in this session** | There is no Attio MCP server or API access here, and direct egress to `api.attio.com` is refused by the network policy. Until that is sorted, use the spreadsheet fallback in `.claude/gtm/attio-schema.md` and load into Attio by hand. |
| Attio native Gmail sync | **Unverified** | The brief assumes it catches Austin's sent mail. Confirm once with a real send before relying on it, since the CRM rules depend on sent mail landing on records without the agent doing it. |
| Calendly to Attio via Zapier | **Unverified** | If the Zap is not live, demo bookings need manual confirmation. Check before the first meeting gets booked, not after. |
| Gmail | Connector available | Only ever used to read replies and to stage drafts. Never to send outbound without Austin. |
| Web search and page fetch | **Restricted here** | Direct fetches to `google.com` and to provider APIs were refused by the egress policy in this environment. Free-web-search sourcing is the whole first step of the sourcing order, so this agent needs a session with open egress to do real list building. |
| Apollo, Hunter, Clay | No credentials configured | Deliberate. Nothing should be able to spend a credit without Austin, and the absence of credentials is a useful second lock on top of the approval rule. |

Short version: the rules are written down and the state files are ready, but this agent
cannot do a real list build until the skill stack is installed and it runs somewhere with
open network egress and an Attio path.

## Blocked on Austin

1. **Chanty closed-won data.** Needed for two things. It recalibrates the provisional buying
   power thresholds in `references/lists-and-icp.md`, and it feeds
   `icp-lookalike-expansion`. Every non-healthcare vertical is paused until it arrives.
   Useful shape: company name, size, industry, how they were sourced, what they replaced,
   who signed, and how long the cycle took.
2. **Agent 2.** The original brief says the system has two agents. Only Agent 1 was written
   down. Nothing has been assumed about the second one.
3. **Follow-up cadence.** The brief covers first touches. No sequence timing exists yet, so
   the agent stages first touches only.

## State and git

`state/run-log.md`, `state/send-queue.md`, `state/open-approvals.md` and
`state/credit-log.md` are the agent's memory. They only work if each run commits them. A run
that stages twenty emails and leaves the queue uncommitted will re-source and re-draft the
same people next time.

## The three locks, restated

Worth repeating outside the SKILL file because they are the things that cost real money or
real reputation if they slip.

1. **No auto-send.** The agent stages. Austin sends.
2. **No unapproved credit spend.** Free search first, gaps batched, one question, then wait.
3. **No inferred stage advancement.** Past `Meeting Booked`, a human confirms.
