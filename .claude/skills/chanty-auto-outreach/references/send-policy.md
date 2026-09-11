# Send policy, auto-send

This agent sends without a human checking each email, so these are hard gates rather than
guidance. A contact that fails any check is held and reported. Nothing is rewritten to get
past a gate.

## Windows

Set by Austin on 2026-09-11, replacing the recipient-local scheme. **One clock, his.**
America/Chicago, weekdays only, never on a US federal holiday.

| Block | Window, Central | Volume |
|---|---|---|
| Morning | 09:00 to 12:00 | 30 |
| Afternoon | 13:00 to 16:00 | 30 |

The recipient's time zone no longer gates sending, and an unknown time zone no longer holds
a contact.

It still matters for one thing: the meeting ask names a specific time, and that time should
be in the reader's zone where it is known. Where it is not known, name the time in Central
and say so, "10am Central". Never state a time with no zone attached and never guess a zone
from an area code.

Worth knowing what this trades away. A 9am Central send lands at 7am on the West Coast and
10am on the East, so some of the volume arrives before the reader's day starts. That is
Austin's call and it buys a much simpler schedule.

## Batching and spacing

Sixty evenly spaced sends is a machine signature. Both blocks go out in **batches**.

One batch per hourly wake. Six wakes a day, six batches, ten emails each.

| Block | Wakes, Central | Batches | Per batch |
|---|---|---|---|
| Morning, 09:00 to 12:00 | 09, 10, 11 | 3 | 10 |
| Afternoon, 13:00 to 16:00 | 13, 14, 15 | 3 | 10 |

Within a wake, spread the ten across the hour rather than firing them on arrival.

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

## Volume

**60 a day from day one, 30 per block.** Austin overruled the warmup ramp on 2026-09-11,
having been told what it was for. There is no ramp.

The reason it was proposed still stands and is now a risk rather than a safeguard: this is
his working mailbox, the domain carries his real business mail, and 60 cold sends a day from
a standing start is a lot for an address with no cold-send history of its own. The warmup
service running alongside helps. The bounce switches below are now the only brake, so they
matter more, not less.

## Send-eligibility gate

Every box, every email, every time.

- [ ] Address is **verified**, or a published role inbox. `extrapolated`, `guessed`,
      catch-all and accept-all all fail. A provider returning an address is not the same as
      finding one, per `.claude/gtm/sourcing-and-credits.md`.
- [ ] Recipient is not in `state/suppression.md`
- [ ] Recipient has never bounced
- [ ] The send falls inside a window on a weekday, Central
- [ ] Nobody else at this company has been emailed by any agent in the last 7 days
- [ ] This person has not been emailed by any agent in the last 14 days
- [ ] Draft cleared all five copywriting stages and the vertical's opening formula
- [ ] Subject line 10 words or fewer
- [ ] CTA is a direct meeting ask with a specific time, carrying a time zone. The reader's
      zone where it is known, Central and labelled where it is not
- [ ] No named competitor anywhere in the body
- [ ] The opening matches the contact's industry, per `copy.md`. An all-desk company fits
      neither approved reason and is held rather than sent

## Follow-up

One follow-up, **three business days** after the first touch. Weekends do not count.

Sent only when all of these hold: no reply of any kind, no bounce, not suppressed, contact
still at the company. One follow-up per contact, ever. There is no third touch until Austin
defines one, and the agent does not invent one.

Follow-ups come out of the same daily cap. They are not extra.

## The mailbox is not this agent's alone

`austin@chanty.com` carries three streams of outbound, and two of them are not this agent's.

1. **A warmup service.** Runs roughly hourly, subjects ending in `- wbx xxx`, labeled
   `Label_1`, to seed domains like stashflowpartners.com, xcelltiming.com, advently.net,
   sprayshoes.com and nichefully.org. Templated replies come back within minutes, often
   signed with a name that has nothing to do with the recipient.
2. **Austin's own manual batches**, sent from the same address.
3. This agent.

Two consequences, both handled below.

### Never read warmup traffic as a reply

A reply counts only when the sender address appears in this agent's own
`state/sent-log.md`. That whitelist is the rule. Everything below is a second layer in case
the log is incomplete:

- Ignore anything labeled `Label_1`.
- Ignore any subject matching `- wbx ` followed by three letters.
- Ignore anything from a known warmup seed domain.
- Treat a reply arriving under 10 minutes after the send as suspect and check it by hand.

Marking a warmup seed as `Replied` in Attio would put fake contacts into the pipeline and
stop a real sequence. Check the whitelist before writing any stage change.

### Count only this agent's own sends

The daily cap, the batch counts and the trailing bounce rate are all computed from
`state/sent-log.md`, never from the mailbox. Warmup traffic would otherwise inflate the
volume and dilute the bounce rate into meaninglessness.

The reverse also matters: the cap counts this agent's sends, but total mailbox reputation is
shared. If Austin runs a manual batch the same day, the real volume on that address is his
plus the agent's plus the warmup. Report the agent's number and say it is not the whole
picture.

## List quality comes before volume

A manual batch of about 20 on 2026-09-09 produced at least three hard bounces: an unknown
recipient at agroliquid.com, an address not found at dsainc.com, and a permanent failure at
therigy.com. That is over 10% against a 3% kill switch, so a list of that quality halts this
agent on its first run.

So verification is not a formality here:

- Nothing sends to an address that has not cleared the gate below. `extrapolated`, `guessed`
  and catch-all all fail, whatever a provider says.
- Prefer a published address over a provider-supplied one, every time.
- On the first three days of sending, stop and report if the bounce rate on the agent's own
  sends exceeds 2%, rather than waiting for the 3% switch. With no ramp, these three days
  are the only early warning there is.
- A bounce is logged against the source that supplied the address, so a provider producing
  bad addresses becomes visible rather than being averaged away.

## Kill switches

Checked at the start of every run, before anything is sent. A tripped switch halts **all**
sending, not just the offending contact, and stays tripped until Austin clears it.

| Trip | Threshold | Action |
|---|---|---|
| Bounce rate | over 3% of the trailing 100 of **this agent's own** sends | Halt everything, report |
| Bounce rate, first 3 days of sending | over 2% | Stop and report before the 3% switch |
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
