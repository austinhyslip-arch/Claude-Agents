# Setup and operating notes

## How the agent gets invoked

- **On-demand:** ask for a competitive check in any session where this repo is checked out
  ("run a competitive check on the last 24 hours"). The skill loads from
  `.claude/skills/chanty-competitive-intel/`.
- **Weekly:** a scheduled Routine fires every Monday and runs the same skill in a fresh
  session. The Routine prompt has to be standalone — a fresh session starts with no
  context — so it should read roughly:

  > Run the Chanty competitive intelligence weekly digest. Read
  > `.claude/skills/chanty-competitive-intel/SKILL.md` in the corgi-comms repo and follow
  > it end to end for the prior 7 days. Include the monthly discovery pass if this run is
  > the digest closest to the 1st. Email the result to austinhyslip@gmail.com and commit
  > the updated state files.

  Suggested schedule: Mondays 13:00 UTC (`0 13 * * 1`), which is 9am ET / 6am PT.

## Dependencies this agent needs at run time

| Dependency | Status as of this commit | Notes |
|---|---|---|
| Gmail send | **Connector installed but not enabled in-session** | Must be enabled for the session (or Routine) that runs the digest, or step 7 falls back to writing the digest to a file. |
| Web search | Available | Primary gathering tool. |
| Direct page fetch | **Blocked by network egress policy in the current remote environment** | `slack.com`, `clickup.com`, `notion.com`, `basecamp.com` and others were refused. Where direct fetch is blocked, pricing and changelog checks fall back to search results, which is weaker for exact price diffs — run the digest in an environment with open egress if pricing accuracy matters. |
| `research` skill | Not installed here | The workflow in SKILL.md is self-contained; if `research` is installed it can do the source gathering in step 2-4. |
| `outbound-triggers-6`, `outreach-4-categories` | Not installed here | `references/signal-rubric.md` carries a standalone version of the scoring. |
| Attio | Not used | By design. This agent writes no CRM records. |

## State and git

`state/run-log.md` and `state/tier3-candidates.md` are the agent's memory. They only work
if each run commits its updates — a run that emails the digest but leaves state uncommitted
will re-report the same items next week.
