# Send policy, auto-send

This agent sends without a human checking each email, so these are hard gates rather than
guidance. A contact that fails any check is held and reported. Nothing is rewritten to get
past a gate.

## Windows

Both blocks are in the **recipient's local time zone**, weekdays only, never on a US federal
holiday.

| Block | Window | Volume at full ramp |
|---|---|---|
| Morning | 08:00 to 12:00 | 30 |
| Afternoon | 13:00 to 16:00 | 30 |

An unknown time zone is held, never guessed from an area code.

## Batching and spacing

Sixty evenly spaced sends is a machine signature. Both blocks go out in **batches**.

| Block | Batches | Per batch | Gap between batches |
|---|---|---|---|
| Morning, 240 min | 6 | 5 | 30 to 50 min, randomized |
| Afternoon, 180 min | 6 | 5 | 20 to 40 min, randomized |

Rules that keep it from reading as automated:

- Randomize the gap between batches inside the range, fresh every day. Never a fixed
  interval.
- Randomize recipient order within a batch, and leave 20 to 90 seconds between individual
  sends inside one.
- Never send on a round minute. No 09:00:00, no 10:30:00.
- Never send the same subject line twice inside one batch.
- Skip a batch outright once or twice a week, at random. Perfect daily consistency is itself
  a tell.
- Never start the first batch at the top of the window. Start 3 to 20 minutes in.

## Ramp

| Week | Daily cap | Per block |
|---|---|---|
| 1 | 20 | 10 |
| 2 | 40 | 20 |
| 3 onward | 60 | 30 |

Austin asked for 60 a day from day one. The ramp is a warmup on a mailbox that has never
sent cold volume, and it protects the address he actually works from. He can overrule it.

## Send-eligibility gate

Every box, every email, every time.

- [ ] Address is **verified**, or a published role inbox. `extrapolated`, `guessed`,
      catch-all and accept-all all fail. A provider returning an address is not the same as
      finding one, per `.claude/gtm/sourcing-and-credits.md`.
- [ ] Recipient is not in `state/suppression.md`
- [ ] Recipient has never bounced
- [ ] Time zone known, and the slot falls inside a window on a weekday
- [ ] Nobody else at this company has been emailed by any agent in the last 7 days
- [ ] This person has not been emailed by any agent in the last 14 days
- [ ] Draft cleared all five copywriting stages and the vertical's opening formula
- [ ] Subject line 10 words or fewer
- [ ] CTA is a direct meeting ask with a specific time in the recipient's local time
- [ ] No named competitor anywhere in the body
- [ ] For a non-healthcare vertical, the generic opening has Austin's sign-off

## Follow-up

One follow-up, **three business days** after the first touch. Weekends do not count.

Sent only when all of these hold: no reply of any kind, no bounce, not suppressed, contact
still at the company. One follow-up per contact, ever. There is no third touch until Austin
defines one, and the agent does not invent one.

Follow-ups come out of the same daily cap. They are not extra.

## Kill switches

Checked at the start of every run, before anything is sent. A tripped switch halts **all**
sending, not just the offending contact, and stays tripped until Austin clears it.

| Trip | Threshold | Action |
|---|---|---|
| Bounce rate | over 3% of the trailing 100 sends | Halt everything, report |
| Hard bounce | any single one | Suppress that address permanently, keep sending |
| Spam complaint | any, ever | Halt everything, report immediately |
| Opt-out request | any, however worded | Suppress permanently, pull colleagues from the queue, flag the company |
| Gmail send failure | 3 in one block | Halt the block, report |
| Reply from a contact | any | Stop that contact's sequence, no follow-up |

Suppression is permanent and never reversed by an agent.

## Logging

Write to `state/sent-log.md` **before** moving to the next recipient, not in one batch at the
end. A crash mid-block must not be able to double-send. Every line carries recipient, Attio
record, address, subject, timestamp with time zone, block, batch number and touch number.
