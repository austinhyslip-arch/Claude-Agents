# Setup and operating notes

## How the agent gets invoked

- **On-demand:** ask for a competitive check in any session where this repo is checked out
  ("run a competitive check on the last 24 hours"). Daily is fine.
- **Weekly:** a Routine fires Monday mornings and runs the same skill in a fresh session.

### The Routine

- Trigger id: `trig_01Dk5VV4fWtEDQ2A2thm2Erc` ("Chanty Weekly Competitive Digest")
- Schedule: `0 13 * * 1` UTC = **08:00 Monday, America/Chicago**, correct while Central is
  on CDT.
- **Must change to `0 14 * * 1` on Nov 1, 2026**, when Central returns to CST, and back to
  `0 13 * * 1` on Mar 14, 2027. Claude Code Routines take UTC cron only, so this cannot be
  set once and forgotten. Each weekly run checks its own firing time against 08:00 Central
  and reports drift rather than silently running an hour off.
- Fires a fresh session each week, so its prompt is standalone: it attaches this repo,
  reads `SKILL.md`, and follows it end to end.

## Dependencies at run time

| Dependency | Status | Notes |
|---|---|---|
| Gmail send | Verified working (test send Aug 21, 2026) | The connector must be enabled for the session or Routine that runs the digest. |
| Gmail **attachments** | **Unverified** | The whole digest design assumes the HTML goes out as an attachment. If the Gmail tool in the session has no attachment parameter, `references/digest-format.md` defines the fallback chain: Google Drive link, then inline plain text. Worth confirming once before relying on a Monday send. |
| Google Drive | Connector available | Fallback host for the HTML file when attachments are unavailable. |
| Web search | Available | Primary gathering tool. |
| Direct page fetch | **Blocked in the remote environment used so far** | `slack.com`, `clickup.com`, `notion.com`, `basecamp.com`, `g2.com` and `capterra.com` were all refused by the network egress policy. That guts two things the spec asks for: pricing verified against the live page, and G2/Capterra review harvesting. Run the weekly somewhere with open egress, or expect the pricing section to stay secondary-sourced and the feature-complaint section to stay thin. |
| `research` skill | Not installed | The workflow is self-contained; the skill is used for gathering when present. |
| `outbound-triggers-6`, `outreach-4-categories` | Not installed | `references/signal-rubric.md` carries a standalone version of the scoring. |
| Attio | Not used | By design. This agent writes no CRM records. |

## State and git

`state/run-log.md`, `state/tier3-candidates.md` and `state/digests/` are the agent's memory
and archive. They only work if each run commits its updates — a run that sends the digest
but leaves state uncommitted will re-report the same items next week.
