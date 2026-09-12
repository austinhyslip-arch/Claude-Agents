# Today's run marker

Liveness signal for the morning run. The 7:00am retry reads this to decide whether the
6:00am run is alive, dead, or never started. Nothing else depends on it.

The container is rebuilt every firing, so this file only means anything if it is
committed and pushed. Write it early, update it at each phase, push every time.

## How the daily run uses it

1. On start, before any sourcing, overwrite this file with today's date, a `started`
   status and the UTC timestamp. Commit and push immediately.
2. At each phase boundary, update `status` and `heartbeat` and push again. Phases:
   `started`, `sourcing-municipal`, `sourcing-manufacturing`, `qualifying`,
   `digest-built`, `digest-sent`, `attio-pushed`, `complete`.
3. A stale heartbeat is what tells the retry the run died partway.

## How the retry uses it

- Marker missing, or its date is not today: the 6:00am run never started. Retry runs a
  full pass.
- Heartbeat older than 40 minutes: the run started and died. Retry takes over.
- Heartbeat fresh: the run is alive. Retry exits without doing anything.
- Status is `digest-sent`, `attio-pushed` or `complete`: the morning already succeeded.
  Retry exits.

## Current state

```
date:
status:
heartbeat:
runner:
note:
```
