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

## Ground truth for claims

Every factual claim about Chanty comes from `value-prop.md`. Price, plan, feature,
compliance, stat, logo, all of it. A number that is not in that file does not exist, and no
agent invents one to fill a sentence. Cite its stats as Chanty's own reported figures, never
as independently verified.

Two live cautions from that file: the `<60% decrease in frontline turnover` figure is
ambiguous and stays out of outbound until Austin confirms what it means, and the big-name
logos are team-level usage rather than enterprise deployments, so they are social proof and
nothing more.

## Rules that override the pipeline

These come from Chanty's own send performance, so where a skill's default disagrees, the
rule below wins.

**Open founder-first.** Austin writes as **the** co-founder of Chanty, not "a", and the
email says so in the first line. It is the strongest thing available that needs no
sourcing, and it earns the direct meeting ask. The shape is: who he is, why Chanty was
built, what that means for the reader, then the ask.

Founder-first is a **frame, not a substitute for an angle.** It answers why she should
listen to him. One specific, sourced sentence still has to answer why her and why now. An
email carrying the founder line and nothing specific about the reader is a template, and
`personalization-playbooks` still decides how much personalization the category earns.

**The healthcare opening, word for word.** Superseded 2026-09-02 by the version below,
built and approved across a 67-contact batch rather than one individual draft. The original
per-account version (item 3 was a sourced, account-specific bridge sentence) is kept at the
bottom of this section for history — it is what Agent 2 used for one-off targets like Amy
Overstreet before this batch, and remains a legitimate fallback when a real per-account
signal exists and is worth using instead of the anecdote below.

**Current standing formula, every healthcare first touch, verbatim except the greeting name
and the day/time/timezone in the ask:**

```
{FirstName},

I'm Austin, co-founder of Chanty, an internal chat tool. We built it because the big
platforms weren't made for clinics needing something simple, affordable, and HIPAA
compliant.

I used to work at a family-run clinic. Group texts, nobody sure who saw what, and constant
HIPAA worry. If you're on a bigger platform, you're over-paying for complicated compliance.

Our base plan means no complex builds or weeks-long integration, just a signed BAA, HIPAA
compliance, and pricing that stays affordable. Need something? Call me, not a bot.

I'm excited to show this to you because it's exactly what I wish I had at the clinic I
worked for. Do you have 15 minutes {Day} at {Time} {TZ}?

Austin
```

119 words including the greeting name, for every recipient — this is the hard ceiling in
the Length and shape section, "under 120," not "up to 120," so there is no headroom to add
anything without cutting something else first.

**This paragraph is deliberately universal, not account-specific.** It carries no company
name, no specialty, no location, no signal. That is not a personalization-honesty violation,
since it never pretends to be about the reader specifically — it is Austin's own true story,
told the same way to everyone, which is a different and legitimate thing from inventing a
fake per-account detail. It does mean this template supplies none of the "one sourced,
personal sentence" the general framework elsewhere in this file still asks for. Where a real
account-specific signal exists and is strong, use the original per-account version below
instead of this one — don't force both into one email.

**Subject line: running as an A/B test, both sentence case, no "Re:".**

- A: "a HIPAA compliant chat"
- B: "we built an affordable HIPAA compliant chat"

Split evenly across a batch. Austin's first draft of both used "Re:" and Title Case; both
violate the standing subject rule above (no fake "Re:", sentence case) and the "Re:" one was
flagged as a real deliverability and CAN-SPAM concern, not just a style note. Austin did not
push back on removing it, so the versions above are what shipped. If he explicitly wants
"Re:" restored on a future batch, that requires him saying so again, not defaulting back to
it.

**Deliberate exception to the comma-list rule**, carried over from the prior version: the
value line ("no complex builds, no weeks-long integration, a signed BAA, HIPAA compliance,
and pricing that stays affordable") is a comma list, which is exactly the pattern the
pipeline otherwise cuts. Austin dictated this wording specifically, so it stands as written
for this one claim block and nowhere else.

---

**Original per-account version, kept as a fallback:**

1. "I'm Austin, the co-founder of Chanty."
2. The reason, close to verbatim: "We built it because the big internal communications
   platforms aren't built for healthcare clinics who need a simple, easy to use platform
   that's affordable."
3. One sentence that reformats to the specific account: their scale, their structure,
   their own signal, whatever `personalization-playbooks` picked for this contact. This is
   the only sourced, personal sentence in the email, and it still has to earn its place.
   It exists to connect the general reason above to this reader, not to repeat either.
4. The value line, in this order and close to this wording: **no price point stated, say
   "base plan"**, then no complex builds, no weeks-long integration, a signed BAA, HIPAA
   compliant, and affordable. Pillar 5 in `value-prop.md` is what backs every claim in it.
5. The direct meeting ask, per the CTA rule below.

**CTA.** Direct meeting ask with a specific time suggested. "Do you have 15 minutes
Thursday at 10 your time?" is the shape. Soft asks lose. Banned: "worth a reply?", "open to
learning more?", "is this a priority for you?", "let me know if you'd like info", and any
CTA that asks the reader to define the next step themselves.

**Subject line.** Three to six words. Ten is the hard ceiling and hitting it means the line
needs another edit. Lowercase or sentence case, not title case. No brackets, no emoji, no
"Re:" that is not a real reply, no question mark trying to look like a thread.

**Value proposition.** Lead with the outcome for the person reading it, drawn from the
persona-mapped pitch angles in `value-prop.md` section 4.

**Never frame a first touch against a named competitor.** Not "better than Slack", not
"cheaper than Teams", not "unlike Monday.com". If the reader wants that comparison they will
ask for it on the call. Naming a competitor in a first touch reads as a pitch and gets
treated as one, and picking the wrong incumbent is worse than picking none.

This holds even though `value-prop.md` marks Chanty's own Slack and Teams data-ownership
lines as safe to use verbatim. Those are available **from the reply onward**, and in
objection handling, content and sales collateral. They are not available in a first touch.
The category critique survives without the name: "the big platforms" does the same work.

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

## Hedge the problem sentence

We do not know how the reader works. The sentence that names their problem is a guess
however good the research was, so it gets written as one.

- "aren't sitting at a computer" becomes "aren't always at a computer"
- "you're losing hours to this" becomes "this more than likely costs you hours"
- "your staff never see the message" becomes "the message probably doesn't reach everyone"

Use "more than likely", "aren't always", "probably", or put it as a question. Anything that
tells a stranger how their own operation runs invites them to correct you instead of reply
to you, and being wrong once costs the whole email.

The facts stay firm. Four offices is four offices, and a posted job is a posted job. It is
the inference drawn from the fact that gets hedged.

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
