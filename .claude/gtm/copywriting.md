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

**The opening, word for word.** Set by Austin on 2026-09-02 and extended on 2026-09-11 to
cover every vertical. Five beats, and **the agent picks line 2 from the industry**.

1. "I'm Austin, the co-founder of Chanty."
2. The reason. Two approved versions, chosen by industry:
   - **Healthcare**, close to verbatim: "We built it because the big internal communications
     platforms aren't built for healthcare clinics who need a simple, easy to use platform
     that's affordable."
   - **Every other industry with a non-desk workforce**, plumbing, trucking, distribution,
     field services, retail, hospitality and the rest: "We built it because the big internal
     communications platforms aren't built for companies whose people are spread across
     sites and mostly aren't at a desk, and who want something simple and affordable."

   There is no third version. An account where everyone works at a desk all day fits neither
   line, and per `icp.md` it is a weak fit anyway, so hold the contact rather than inventing
   a reason that does not apply to them.
3. One sentence that reformats to the specific account: their scale, their structure,
   their own signal, whatever `personalization-playbooks` picked for this contact. This is
   the only sourced, personal sentence in the email, and it still has to earn its place.
   It exists to connect the general reason above to this reader, not to repeat either.
4. The value line, in this order and close to this wording. It says "base plan" rather than
   naming a tier, and it **ends with the price**, set by Austin on 2026-09-11:
   - **Healthcare**: "Our base plan: no complex builds, no weeks-long integration, BAA
     signed, HIPAA compliant, and affordable at $3 a user."
   - **Every other industry**: "Chanty is team chat and tasks that runs on a phone. Our base
     plan: no complex builds, no weeks-long integration, and affordable at $3 a user."

   BAA and HIPAA are dropped outside healthcare because they mean nothing there, which is
   why the non-healthcare line is three parts rather than five. Pillar 5 in `value-prop.md`
   backs the compliance claims, Pillar 1 backs the price.
5. The direct meeting ask, per the CTA rule below.

**Deliberate exception to the comma-list rule.** Item 4 is a comma list, which is exactly
the pattern the pipeline otherwise cuts. Austin dictated this wording specifically, so it
stands as written for this one claim block and nowhere else. Do not generalize it into
permission for comma lists elsewhere in the email, and do not soften or shorten Austin's own
phrasing here without him saying so again.

**On the price.** It appears in the body of every email, in this line, whatever the subject
line test is doing. $3 a user is the annual billing figure from the pricing page, and it is
$4 paid monthly. Never quote $3 as the monthly price.

**CTA.** Direct meeting ask with a specific time suggested. "Do you have 15 minutes
Thursday at 10 your time?" is the shape. Soft asks lose. Banned: "worth a reply?", "open to
learning more?", "is this a priority for you?", "let me know if you'd like info", and any
CTA that asks the reader to define the next step themselves.

**Subject line.** Austin confirmed the competitor ban holds in subject lines and first
touches on 2026-09-11. Agent 3 carries the fuller subject rules in its own `copy.md`:
sentence case, plain, no brand, product category for a named person and a plain question for
a role inbox. The problem-fragment style is retired everywhere.

Three to six words. Ten is the hard ceiling and hitting it means the line
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
