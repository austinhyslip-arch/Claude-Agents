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

## Search demand signals

`references/search-demand.md` is the sub-spec: taxonomy, sources, what earns a row, and the
handoff to the content idea agent. Two things to know before the first run:

- The Google Chat keyword set ships **defined but disabled** in `references/search-terms.json`.
  Flip `"enabled": true` once a weekly run has come back clean.
- The content idea agent reads `.claude/shared/content-gaps.json`. That agent does not exist
  in this repo yet; the file and its contract (`.claude/shared/README.md`) are written
  regardless, so the data is already accumulating when it arrives.

Run `python3 scripts/selftest.py` after touching anything in `scripts/` — it exercises the
whole pipeline against fixtures, offline, in about a second.

**First live run, Aug 26, 2026 — no usable data.** All 29 terms pulled; both sources
unavailable in this environment. `trends.google.com` is blocked by the egress policy, and
the Custom Search credentials are not set here. The pipeline behaved correctly: it gave up
on each source after three identical failures, wrote the reason into every row and into the
run caveats, and finished in 92 seconds rather than grinding through 29 rounds of backoff.
Nothing was cached, so the first real run still starts from a clean baseline. To get real
data the weekly needs an environment with `trends.google.com` allowed, and the Custom
Search key set — with the key alone the SERP half runs and `--no-trends` is the honest
switch until the host is unblocked.

## Dependencies at run time

| Dependency | Status | Notes |
|---|---|---|
| Gmail send | Verified working (test send Aug 21, 2026) | The connector must be enabled for the session or Routine that runs the digest. |
| Gmail **attachments** | **Unverified** | The whole digest design assumes the HTML goes out as an attachment. If the Gmail tool in the session has no attachment parameter, `references/digest-format.md` defines the fallback chain: Google Drive link, then inline plain text. Worth confirming once before relying on a Monday send. |
| Google Drive | Connector available | Fallback host for the HTML file when attachments are unavailable. |
| Web search | Available | Primary gathering tool. |
| Direct page fetch | **Blocked in the remote environment used so far** | `slack.com`, `clickup.com`, `notion.com`, `basecamp.com`, `g2.com` and `capterra.com` were all refused by the network egress policy. That guts two things the spec asks for: pricing verified against the live page, and G2/Capterra review harvesting. Run the weekly somewhere with open egress, or expect the pricing section to stay secondary-sourced and the feature-complaint section to stay thin. |
| `pytrends` | Installs cleanly; **endpoint blocked in the remote environment** | `python3 -m pip install -r scripts/requirements.txt` works. But `trends.google.com` is refused by the same egress policy that blocks the pricing pages — the proxy answers 403 to CONNECT. Verified Aug 26, 2026: a full 29-term run returned no trend data at all. Unofficial library besides; upgrading pytrends is the first fix to try when Google changes the backend. Its failures degrade rows, never the build. |
| Google Custom Search API | **Reachable — key not set** | `www.googleapis.com` passes the egress policy (verified Aug 26, 2026: Google itself answered, rejecting the call for having no key). So the SERP half is one credential away from working here. Set `GOOGLE_CSE_API_KEY` and `GOOGLE_CSE_CX` — the same credentials social listening uses. Free tier is 100 queries/day; a weekly run is 29. |
| `research` skill | Not installed | The workflow is self-contained; the skill is used for gathering when present. |
| `outbound-triggers-6`, `outreach-4-categories` | Not installed | `references/signal-rubric.md` carries a standalone version of the scoring. |
| Attio | Not used | By design. This agent writes no CRM records. |

## State and git

`state/run-log.md`, `state/tier3-candidates.md`, `state/digests/`, `state/search-demand/`,
`state/search-demand-cache.json` and `state/serp-history.jsonl` are the agent's memory and
archive. The cache is what gives the trend arrows something to compare against — a run that
doesn't commit it starts cold the following week and falls back to the in-series
comparison. They only work if each run commits its updates — a run that sends the digest
but leaves state uncommitted will re-report the same items next week.
