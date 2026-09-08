# The Daily Routine

Set up 2026-09-08 at Austin's request.

    Trigger id    trig_01KLdpPqeoePnCH5N8ytHmRk
    Name          Chanty ecosystem agent, daily run
    Schedule      12 12 * * *  (UTC)
    Local time    07:12 America/Chicago while CDT is in effect
    Mode          fresh session per firing
    Notifications push on, email off

Every firing starts from nothing, so the prompt is written as a complete
standalone instruction rather than as a continuation. It names the repository and
branch, points at `CLAUDE.md` and `workflows/daily-operation.md`, and restates the
rules that do not bend.

## What it does each morning

One category slice, rotating through `pilot/targeting-plan.md` from wherever the
last run log left off. Discovery, dedupe, research, scoring, qualification,
public contact discovery, opportunity, signals, drafts into Gmail, gate
validation. Then it stops.

It finishes by running `eco send-window --drafts-only` and reporting which drafts
can go out now and when the rest open, because Austin sends them by hand and that
is the information he needs to do it.

It writes a run log to `pilot/run-<date>-<category>.md` and pushes it.

## Two things to know

**Daylight saving.** Cron is UTC and does not move. `12 12 * * *` is 07:12
Central now, and becomes 06:12 Central when CST starts in November. Shift it to
`12 13 * * *` then, or leave it if an earlier run is fine.

**Connectors.** The `connectors` parameter is not available for this
organization, so the routine was created without a stored connector grant. The
tool warned that fired sessions may therefore run without `mcp__Gmail__*` and
`mcp__Attio__*` tools. If a run reports it cannot reach Gmail, the fix is to
attach the connectors to this routine in the claude.ai Routines UI, which can do
what this tool could not.

Everything else in the run works without connectors: discovery, research,
scoring, gating and the run log are all local. Only the final step of writing the
draft into Gmail needs one.

## Send windows in the daily report

The run ends with `eco send-window --drafts-only`, which is the list Austin acts
on. Three shapes of answer:

- a resolved zone, so 08:00-17:00 in that zone
- an estimated zone, so 09:00-16:00, narrowed because an hour of error should
  not put a message outside someone's day
- no zone, so the noon Central hour, which is inside business hours everywhere
  in the US

## Changing it

    list_triggers                          find it again
    update_trigger  trig_01KLdpPqeoePnCH5N8ytHmRk   change schedule, prompt or enabled
    delete_trigger  trig_01KLdpPqeoePnCH5N8ytHmRk   stop it

Pausing is `enabled: false`, which keeps the run history. Deleting loses it.
