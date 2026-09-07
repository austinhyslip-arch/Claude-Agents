# Suppression

Suppression is permanent until a human changes the record. No agent may lift a
suppression. Not the Learning Agent, not a new signal, not a leadership change.

## Suppression scopes
- `contact` — this person only
- `organization` — the organization and every contact at it
- `domain` — every organization on the domain

## Reasons
- `requested_no_contact` — they asked. Permanent, no exceptions.
- `complaint` — permanent, and escalate to a human on entry.
- `unsubscribed` — permanent for automated sending.
- `competitor` — organization level.
- `partner_conflict` — human set.
- `bounced_hard` — contact level, email marked invalid.
- `manual` — human set, reason recorded in the record.

## Enforcement
Suppression is checked at three points and every one of them fails closed:
1. Before a contact record is created
2. In the hard qualification gates
3. In the send gate, immediately before any message leaves

`tests/test_suppression.py` asserts a suppressed contact cannot reach the send
queue through any path.

## Opt-out processing
An opt-out is written to suppression the same day it arrives, before anything else
is done with the reply.
