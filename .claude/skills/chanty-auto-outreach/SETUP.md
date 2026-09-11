# Setup, auto-outreach

## Scheduling

Austin set the windows to **his own clock** on 2026-09-11: 9am to 12pm and 1pm to 4pm
Central, weekdays, regardless of where the recipient is. Six hourly wakes, ten emails each,
60 a day.

### The two Routines

| Routine | Cron (UTC), while Central is on CDT | Covers |
|---|---|---|
| Send and sweep | `0 14-16,18-20 * * 1-5` | 09, 10, 11 and 13, 14, 15 Central |
| Weekly sourcing | `0 13 * * 1` | Monday 8am Central, an hour before the first send |

### Daylight saving needs a diary note

Dropping the recipient-local scheme made the agent simpler and the cron fragile, because now
the cron is the only thing that knows what time it is. Central shifts and these expressions
have to shift with it.

| Period | Central | Send cron | Sourcing cron |
|---|---|---|---|
| CDT, to Nov 1 2026 | UTC-5 | `0 14-16,18-20 * * 1-5` | `0 13 * * 1` |
| CST, Nov 1 2026 to Mar 14 2027 | UTC-6 | `0 15-17,19-21 * * 1-5` | `0 14 * * 1` |

**Next switch: Nov 1, 2026.** Left alone, the agent would start sending at 8am Central and
stop at 3pm. Not a disaster, but it is an hour outside the window Austin set, so the run
summary should flag the drift rather than quietly running early.

## The Routines, and what Austin has to do to them

Both exist, both carry the right cron and prompt, and **both are disabled**. They are
disabled because a Routine created from inside a Claude Code session cannot be given
connectors on this account. Passing a `connectors` list is refused outright, and one created
without it fires sessions with no Attio, no Apollo and no Gmail. It would wake up, be unable
to read the CRM or send anything, and email noise.

| Routine | Trigger id | Cron (UTC, CDT) |
|---|---|---|
| Chanty Auto-Outreach: send and sweep | `trig_01XMfzADU5cE6hvjfVvWDzpf` | `0 14-16,18-20 * * 1-5` |
| Chanty Auto-Outreach: weekly sourcing | `trig_019udqANGyH3fhh3Aq86RNEZ` | `0 13 * * 1` |

**Austin's three steps, in the claude.ai Routines UI:**

1. Open each Routine and attach the connectors: **Attio, Apollo, Gmail, Google Calendar**,
   and Clay if the paid waterfall is ever wanted.
2. Enable both.
3. Delete the leftover test Routine, `trig_013ngKiZ3Ggg7kMEopVyjVqG`, "TEST self-bind
   connector check (DISABLED, delete me)". It was a check on whether a Routine firing back
   into a live session inherits that session's connectors. The answer was not clear, so it
   was disabled rather than relied on. Deleting it from here was blocked by a permission
   rule.

Nothing sends until step 2. The queue is empty as well, so the first real sends come after
the first sourcing run.

The prompts stored on both Routines are below, for reference and for rebuilding them by hand
if they are ever lost.

### Prompt, send and sweep

```
Run the Chanty auto-outreach send and sweep for this hour.

The repo austinhyslip-arch/Claude-Agents is attached, branch
claude/chanty-gtm-agent-system-yx0gb9. Read .claude/skills/chanty-auto-outreach/SKILL.md
and follow it. Read the shared contracts in .claude/gtm/ first; they outrank the skill
file where they overlap.

Check the kill switches in references/send-policy.md before anything else. If one is
tripped, send nothing, email Austin at austin@chanty.com, and stop.

Send during 09:00 to 12:00 and 13:00 to 16:00 Central, weekdays only. The recipient's own
time zone does not gate sending; it is used only to put a labelled time in the meeting ask. Send one batch
of ten, spread across the hour rather than all at once.
Every email clears the full send-eligibility gate first. Log each send to
state/sent-log.md before moving to the next recipient.

Send the three-business-day follow-up to anyone due, out of the same daily cap.

Then sweep replies. A reply counts only if the sender is in state/sent-log.md. Ignore
anything labeled Label_1, any subject matching "- wbx" plus three letters, and the warmup
seed domains; that traffic is a warmup service, not real prospects. Update Attio for real
replies only, both the person and their company, who_contacted set to Agent 3 (auto-send).

Commit and push the state files. Email Austin only if something needs him: a tripped kill
switch, a real reply, a bounce, or nothing sent when something should have been.
```

### Prompt, weekly sourcing

The prompt stored on the disabled Routine above is the one to reuse. It runs the Source mode
only, sends nothing, works the free source ladder before calling anything a gap, and stops to
ask before spending a credit.

## Before the first real send

1. **Create both Routines in the UI** with connectors attached.
2. **Know that there is no ramp.** Austin overruled it on 2026-09-11 after being told what
   it was for. 60 a day from the first day, on his working mailbox. The bounce switches are
   the only brake left.
3. **Check the warmup service is still running.** It is what is keeping the domain warm
   alongside this, and the reply filter depends on recognising its traffic.
4. **Watch the first three days.** The 2% early trip exists because a manual batch of about
   20 on 2026-09-09 produced at least three hard bounces.

## Dependencies

| Dependency | State |
|---|---|
| Attio | Connected. Companies still has no custom fields, so company-side tracking is in notes. |
| Apollo | Connected. 633 lead credits of 855. Waterfall email and phone both disabled on the plan. |
| Clay | Connected. |
| Gmail | Connected. Sends as austin@chanty.com. |
| Google Calendar | Connected. Used to put a real time in the meeting ask. |
| Routines with connectors | **Blocked from here.** Must be created in the claude.ai UI. |
| Page fetching | Works via curl. The WebFetch tool is still blocked by egress policy. |
