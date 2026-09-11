# Setup, auto-outreach

## Scheduling

"Start at 8am in the recipient's local time zone" cannot be encoded in cron, because cron is
UTC and 8am local is four different UTC hours that both shift at daylight saving. Writing one
Routine per zone means eight Routines that all break twice a year.

So the schedule is deliberately dumb and the agent is smart. **One hourly Routine.** At each
firing the agent reads each queued contact's time zone, works out the local hour, and sends
the batch for any contact currently sitting at 08:00 to 12:00 or 13:00 to 16:00 local. A
contact whose local time is outside both windows is simply not sent to on that wake.

That makes daylight saving a non-event. Nothing in the cron encodes a local time, so nothing
needs changing in March or November.

### The two Routines

| Routine | Cron (UTC) | Covers |
|---|---|---|
| Send and sweep | `0 12-23 * * 1-5` | 08:00 ET through 16:00 PT while the US is on daylight time |
| Weekly sourcing | `0 11 * * 1` | Monday, before the first send window opens |

The send window runs 12:00 to 23:00 UTC because 08:00 Eastern is 12:00 UTC and 16:00 Pacific
is 23:00 UTC during daylight time. On standard time everything shifts an hour later, so the
last Pacific batch lands at 15:00 local instead of 16:00. Still inside the window, so it is
left alone rather than papered over with a second cron crossing midnight.

Sourcing runs at 11:00 UTC Monday, one hour before the first send wake, so the queue is full
before anything goes out.

## The connector problem, and it is a blocker

**Routines created from inside a Claude Code session cannot carry connectors on this
account.** Passing a `connectors` list is rejected outright, and creating one without it
produces a Routine whose fired sessions have no Attio, no Apollo, no Gmail. It would wake up
every hour, be unable to read the CRM or send anything, and email nothing useful.

A sourcing Routine was created this way on 2026-09-11 to test it, confirmed the problem, and
was **disabled rather than left to fire broken**:

- `trig_019udqANGyH3fhh3Aq86RNEZ`, "Chanty Auto-Outreach: weekly sourcing (DISABLED, no connectors)"

**Both Routines have to be created in the claude.ai Routines UI instead**, where connectors
can be attached. Attach Attio, Apollo, Gmail and Google Calendar, and Clay if the credit
waterfall is ever wanted. The prompts below are the ones to paste in.

Delete or re-enable the disabled Routine once the UI versions exist. Leaving both enabled
would double-source every Monday.

### Prompt, send and sweep

```
Run the Chanty auto-outreach send and sweep for this hour.

The repo austinhyslip-arch/Claude-Agents is attached, branch
claude/chanty-gtm-agent-system-yx0gb9. Read .claude/skills/chanty-auto-outreach/SKILL.md
and follow it. Read the shared contracts in .claude/gtm/ first; they outrank the skill
file where they overlap.

Check the kill switches in references/send-policy.md before anything else. If one is
tripped, send nothing, email Austin at austin@chanty.com, and stop.

Work out the local hour for each queued contact from their time zone. Send only to
contacts currently inside 08:00 to 12:00 or 13:00 to 16:00 local, on a weekday. Send one
batch, sized for the current ramp week, spread across the hour rather than all at once.
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
2. **Confirm the ramp.** Week one is 20 a day, not 60. Austin asked for 60 from day one and
   can overrule this, but the mailbox has never sent cold volume from this agent.
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
