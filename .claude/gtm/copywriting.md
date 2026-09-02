# Copywriting contract

One pipeline, run in order. These are not five options to pick from. Each stage hands its
output to the next.

## The pipeline

**1. `b2b-cold-email-copywriting`** sets the core structure. Everything after this edits
that draft rather than starting over.

**2. `cold-email-strategist`** shapes the first touch. What is the reason for this email
landing today, and what is the one thing it is asking for.

**3. `josh-braun-copywriting`** shapes the hook and the psychology. Poke the Bear. The
opening should make the reader recognise a problem they already have rather than announce
a product they have never heard of. No pressure, no manufactured urgency, no flattery
opener.

**4. `frontal-messaging-templates`** is a reference for structure and deliverability only.
Read it for length, formatting and spam-trigger rules. Do not let its voice overwrite the
draft. It is not a competing writer.

**5. `human-mannerisms`** is the final pass. Strip anything that reads as written by a
machine. If a sentence would not survive being read aloud by a person who talks like a
person, it does not ship.

## Rules that override the pipeline

These come from Chanty's own send performance, so where a skill's default disagrees, the
rule below wins.

**CTA.** Direct meeting ask with a specific time suggested. "Do you have 15 minutes
Thursday at 10 your time?" is the shape. Soft asks lose. Banned: "worth a reply?", "open to
learning more?", "is this a priority for you?", "let me know if you'd like info", and any
CTA that asks the reader to define the next step themselves.

**Subject line.** Three to six words. Ten is the hard ceiling and hitting it means the line
needs another edit. Lowercase or sentence case, not title case. No brackets, no emoji, no
"Re:" that is not a real reply, no question mark trying to look like a thread.

**Value proposition.** Lead with the outcome for the person reading it. Never frame the
email against a named competitor. Not "better than Slack", not "cheaper than Teams", not
"unlike Monday.com". If the reader wants that comparison they will ask for it on the call.
Naming a competitor in a first touch reads as a pitch and gets treated as one.

**Tone.** Casual by default. Neutral is the fallback for healthcare and other conservative
verticals. Formal is never right. Practical test: contractions yes, "I wanted to reach out"
no, "Per my previous" never.

## Length and shape

- Under 90 words for a first touch. Under 120 always.
- Short paragraphs, one to two sentences each. No wall.
- One link at most, and often zero. Zero links in the first touch is the safer default for
  deliverability.
- No attachments in a cold first touch.
- No images, no tracking pixel, no HTML signature block on the first send.
- One ask per email. If there are two asks, one of them is a follow-up.

## Things that get a draft rejected

Any of these means the draft goes back through step 5 before it reaches the queue.

- "I hope this email finds you well" or any variant
- "I came across your profile / your website / your company"
- "quick question" as an opener when there is no question
- "circling back", "touching base", "just following up"
- "revolutionary", "seamless", "best-in-class", "game-changing", "leverage", "solutions",
  "empower", "unlock"
- em-dashes
- a compliment the writer cannot back up
- claiming to have read something the agent did not actually read
- any personalization detail that is not verifiable from a source the agent can cite

## Never open on their history

The angle is about the problem they have today. Not their career, not their tenure, not
where they worked before, not how long they have been in the job.

Banned openers, whatever the research turned up:

- "You went from X to Y"
- "You've been at <company> for three years now"
- "I saw you used to work at <company>"
- anything reciting their job history back to them
- anything that reads like their profile was studied

Two reasons. They are not thinking about their old job, so it is not relevant to them. And
it reads like surveillance, which costs more goodwill than the specificity buys.

True and checkable is the floor, not the bar. A detail can pass the honesty rule and still
be the wrong thing to say. The test is whether it is on their mind this week.

## Personalization honesty

The angle has to be real. If `personalization-playbooks` picks an authored-content angle,
there needs to be an actual piece of content with a URL in the record. If it picks a
company trigger, the trigger needs a source and a date. An invented detail is worse than a
generic email, because the reader knows immediately and the domain pays for it.

Where no honest angle exists, the email uses the persona and the industry only, and the
record gets tagged `personalization: generic` so the reply rate can be compared later.
