# Value proposition contract

**This file is ground truth for every claim any agent makes about Chanty.** Written by
Austin and preserved verbatim below the line. If an agent wants to say something about what
Chanty is, costs, does, or has done for anyone, it comes from here or it does not go in the
copy.

## How agents use it

- **Copywriting.** `copywriting.md` runs the pipeline. This file supplies what the email is
  allowed to claim. Feed it to `b2b-cold-email-copywriting` and `josh-braun-copywriting` as
  ground truth, per the note at the top of Austin's document.
- **Competitive intel.** `chanty-competitive-intel` cross-references section 5 when a
  competitor moves, so a pricing or feature change gets read against Chanty's actual
  position rather than a remembered one.
- **Never invent a number.** Every stat in section 3 is Chanty's own reported figure. Cite
  them as "Chanty customers report" and never as independently verified. A number that is
  not in this file does not exist.

## Two rules that resolve conflicts with `copywriting.md`

**1. Named competitors.** `copywriting.md` bans naming a competitor. This file marks the
Slack and Microsoft Teams data-ownership comparisons as safe to use verbatim. Both stand,
split by context:

- **First touch: no competitor named.** The ban holds. Naming one makes the reader evaluate
  Chanty against that product instead of against their own problem, and picking the wrong
  incumbent is worse than picking none.
- **From the reply onward, and in objection handling, content and sales collateral: named
  comparisons are available**, limited to what section 6 and section 7 permit.

**2. Claim precision.** Section 3 writes three internal-comms stats as `>80%`, `>28%` and
`<60%`. The `<60% decrease in frontline turnover` is ambiguous: it could mean up to 60% or
at least 60%. **Do not put that figure in outbound until Austin confirms which it is.** The
healthcare stats in the same table are unambiguous and can be used now.

## What this file does not close

The **Chanty customer win data** gap is still open. Everything here is sourced from
chanty.com, which is site copy and self-reported numbers, not customer stories. The
non-healthcare verticals and `icp-lookalike-expansion` still wait on real closed-won data,
and the caution on the big-name logos in Pillar 8 is exactly why.

---

# Chanty Value Proposition Library

**Purpose:** A single source of truth for value props, proof points, and competitive angles, pulled directly from chanty.com. Built for the copywriting, competitive intel, and content agents in the `swan-gtm/gtm-skills` stack. Feed this into `josh-braun-copywriting` and `b2b-cold-email-copywriting` as ground truth for claims, and cross-reference it in the competitive intel digest.

**Scope note:** This covers the pages that actually carry value prop and proof: homepage, features, pricing, the Slack-alternative page, security, apps/integrations, and a sample of the solution pages (healthcare, internal comms, retail, marketing). The remaining solution pages (IT specialists, logistics, property managers, realtors, restaurants, coaching, education) run the same template with swapped-in vertical language and I didn't pull every one line by line. If you want those mapped out too, say the word and I'll go back through them.

---

## 1. Core positioning

**One-liner:** Chanty is the affordable, all-in-one chat, video, and task platform for small and mid-sized teams who don't want to pay Slack prices, wrestle with Microsoft Teams, or stitch together three separate tools just to talk to each other and track work.

**Elevator pitch:** Most teams end up paying for a chat app, a video tool, and a task manager separately, then losing time bouncing between all three. Chanty puts all of it in one $3/user/month plan, with unlimited message history even on the free tier, HIPAA compliance included at the Business level (not locked behind Enterprise), and a UI simple enough that teams report getting productive in a day instead of a quarter.

**What Chanty is not:** A Slack clone with a lower price tag. The site leans hard on three things Slack and Teams don't do well for SMBs: cost, simplicity, and data ownership.

---

## 2. Value pillars

Each pillar below has the claim, the proof behind it, who it's for, and the competitive angle it unlocks.

### Pillar 1 — Real, provable affordability
**Claim:** $3/user/month billed annually, $4/month if paid monthly. Free plan supports up to 5 team members with no time limit.
**Proof:** Pricing page. Chanty's own comparison language calls its paid plans "twice more affordable compared to Slack chat." A 5-person team on Business runs $180/year annual or $240/year monthly, a number small enough to put directly in a subject line or first line of an email.
**Who it's for:** Budget-owner personas — office managers, ops leads, founders, finance-adjacent buyers who feel Slack or Teams pricing creep every renewal.
**Competitor angle:** Tier 1 (Slack, Teams) price per seat plus the cost of a second tool for tasks. Tier 2 (Asana, Monday, ClickUp, Wrike) price per seat for tasks plus the cost of a separate chat tool. Chanty's pitch is one bill instead of two.

### Pillar 2 — All-in-one, not bolt-on
**Claim:** Chat, group and video calls (up to 1,000 participants, 49 on screen at once), Kanban task boards, calendar, polls, file storage, and a team directory, all native, not a Trello embed or a Zoom add-in.
**Proof:** Features page and homepage. "Turn any message into a task," Kanban board view, screen sharing, built-in calendar and events, polls and forms.
**Who it's for:** Teams tired of context-switching between a chat app and a task app. Especially useful against Tier 2 competitors, since none of Asana, Monday, ClickUp, Basecamp, Notion, or Wrike have native real-time chat or video calling.
**Competitor angle:** Slack has no native task manager. MS Teams tasks (Planner/To Do) is widely seen as a clunky bolt-on. Task-first tools force a second subscription for communication.

### Pillar 3 — Unlimited history on every plan, including free
**Claim:** Unlimited searchable message history, even on the free tier.
**Proof:** Pricing page free-tier feature list; slack-alternative page explicitly leads with this: "Never lose a single message... No limits. No hidden costs."
**Who it's for:** Anyone burned by Slack's free-tier 90-day history cap, or teams that treat chat as institutional memory (support, ops, agencies working across clients).
**Competitor angle:** This is a direct, factual dig at Slack's free-tier limitation and one of the cleanest "objectively better, not just cheaper" claims Chanty has.

### Pillar 4 — Simple enough that nobody needs training
**Claim:** Minimal learning curve, described on-site as a driver of a 55% productivity increase reported by customers.
**Proof:** "Cut the learning curve with interface decluttered from stuff you'll never use" (repeated across multiple pages). App store ratings: 4.9/5 Google Play, 4.7/5 Apple App Store, 4.7/5 Capterra, 4.5/5 G2, 4.7/5 SourceForge, based on 1,000+ combined reviews.
**Who it's for:** Non-technical teams, SMBs without a dedicated IT function, anyone who has watched a team stall out during a Slack or Teams rollout.
**Competitor angle:** MS Teams is widely perceived as heavy and complex for small teams. Slack's feature depth becomes bloat once a team passes a certain size without a dedicated admin.

### Pillar 5 — Enterprise-grade security without enterprise complexity or enterprise pricing
**Claim:** HIPAA compliance and a signed BAA come standard on the **Business plan** ($3/user/month), not gated behind Enterprise. Also on Business: SSO, 2FA, customizable data retention, IP allowlisting.
**Proof:** Pricing page plan comparison. Compliance badges across the site: SOC 2, ISO 27001, ISO 9001, GDPR, DPF, FINRA, C5, HIPAA. Security page details TLS 1.2+, AES-128-GCM, encrypted file storage, penetration testing, isolated team storage.
**Who it's for:** Healthcare, financial services, or any buyer where compliance is a checkbox that usually forces them up to an Enterprise tier elsewhere.
**Competitor angle:** This is probably Chanty's single strongest differentiator against Tier 2 tools, most of which gate HIPAA/BAA behind their top-tier plans. Worth leading with in the healthcare vertical specifically.

### Pillar 6 — Data ownership as a stated principle, not just a policy
**Claim:** On the healthcare page, Chanty states directly: "We do not sell or use your data (as Slack does)" and "We do not train AI on your messages (as MS Teams does)."
**Proof:** Direct quotes, sourced to the healthcare solution page's "Chanty benefits" comparison block. Also echoed on the homepage/security page as "Own Your Data" and "Zero Moderation — no one has direct access to your databases or messages."
**Who it's for:** Any buyer newly wary of AI training on their internal comms, which is a live, current objection given how much Copilot/AI-in-the-workplace anxiety is circulating.
**Competitor angle:** This is a named, on-site comparison to Slack and Microsoft. Safe to use verbatim in copy since it's Chanty's own stated claim, not something invented for a cold email.

### Pillar 7 — Fast to deploy, painless to migrate into
**Claim:** Data import from Slack, MS Teams, and other messengers. Mobile-first design with offline sync. Apps for Windows, Mac, Linux (Debian and Fedora), iOS, and Android.
**Proof:** "Move your team to Chanty" import section, downloads page links, healthcare page's "Cloud or On-Prem" and "Built-In Flexibility" sections mentioning API/EHR integration without "complex integrations required."
**Who it's for:** IT buyers worried about switching costs, and frontline/deskless workforce use cases (retail, healthcare, logistics) where mobile access matters more than desktop.

### Pillar 8 — Proof at scale
**Claim:** Used by 75,000+ companies, with recognizable logos: Oracle, NASA, Tata, Manchester United, Salesforce, MIT, Nike, GovTech.
**Proof:** Homepage logo strip. 1,000+ reviews averaging 4.5–4.9 across platforms.
**Caution for copy:** These are almost certainly individual teams or departments inside these organizations using free or Business-tier seats, not enterprise-wide deployments. Fine to use as social proof ("teams inside companies like Nike and Salesforce use Chanty"), risky to imply as a company-wide enterprise win without more context. Worth confirming before using in an email to a large enterprise prospect who might push back.

---

## 3. Vertical proof points (site-sourced, self-reported by Chanty)

| Vertical | Stat | Source page |
|---|---|---|
| Healthcare | 40% faster response times for care teams | /solutions/healthcare/ |
| Healthcare | 3+ hours saved weekly per staff member on admin tasks | /solutions/healthcare/ |
| Healthcare | 50% fewer unnecessary phone calls | /solutions/healthcare/ |
| Internal comms (general + retail) | >80% employee engagement after adoption | /internal-communications/, /internal-communications-retail/ |
| Internal comms (general + retail) | >28% stronger connection to the company | /internal-communications/, /internal-communications-retail/ |
| Internal comms (general + retail) | <60% decrease in frontline turnover | /internal-communications/, /internal-communications-retail/ |
| Company-wide | 55% more productive (customer-reported) | /features/, /slack-alternative/ |
| Company-wide | 95% saw a boost in employee engagement after switching | homepage, multiple solution pages |

**Flag for the copy pipeline:** these are Chanty's own customer-reported numbers, not third-party audited. Fine to use as proof points in outbound and content ("Chanty customers report...") but don't present them as independently verified statistics if a prospect asks for the methodology.

---

## 4. Persona-mapped value props

Use these as the hook layer before `josh-braun-copywriting` shapes the actual email.

**Economic buyer / Ops lead / Founder (cost-conscious SMB)**
Pain: paying for Slack plus a task tool plus a video tool, watching the bill creep every renewal.
Pitch angle: one $3/seat bill replaces two or three subscriptions, and the free tier is a real, usable product up to 5 people, not a crippled trial.

**IT / Admin buyer**
Pain: compliance requirements block adoption of "simple" chat tools, or migration off Slack/Teams feels like a project.
Pitch angle: HIPAA/BAA, SSO, 2FA, and custom data retention ship on the Business plan, not gated to Enterprise. Native import tools handle the migration.

**End user / employee**
Pain: current tool is cluttered, has a learning curve, or doesn't work well on mobile for frontline staff.
Pitch angle: WhatsApp-simple interface, works offline, same app across desktop and mobile.

**Healthcare buyer (clinical or admin)**
Pain: PHI handling risk, slow interdepartmental communication, phone-tag between shifts.
Pitch angle: 40% faster response times, HIPAA/BAA included, EHR-flexible API, on-prem option for maximum data control.

**Frontline/retail ops leader**
Pain: deskless workforce disconnected from HQ, high turnover, low engagement.
Pitch angle: mobile-first, works on in-store kiosks, >80% engagement and <60% turnover reduction reported after adoption.

**Marketing agency / client-services lead**
Pain: managing communication across internal team plus multiple clients or contractors without leaking channels into each other.
Pitch angle: guest seats (3 free guest seats per paid member on Business), Kanban task boards per client, keeps client threads separate from internal ones.

---

## 5. Competitive angles, mapped to your tier list

**vs. Slack (Tier 1)**
- Half the price on paid plans (Chanty's own claim: "twice more affordable")
- Unlimited message history on the free tier vs. Slack's 90-day cap
- Native task manager, so no second tool needed
- Direct data-ownership claim: "we do not sell or use your data (as Slack does)"

**vs. Microsoft Teams (Tier 1)**
- No M365 dependency required to get value
- Lighter, simpler onboarding, no IT project needed to roll out
- Direct AI-training claim: "we do not train AI on your messages (as MS Team does)," relevant given current Copilot data anxiety
- HIPAA/BAA included at a lower price point than Teams' compliance-tier bundles typically run

**vs. Google Chat (Tier 1)**
- Not addressed anywhere on chanty.com. This looks like a real gap in Chanty's own messaging, worth testing in outbound copy rather than pulling from existing site language. General angle would mirror the Slack/Teams positioning: lower cost, native tasks, no dependency on the rest of a Workspace subscription to get value.

**vs. Asana, Monday.com, ClickUp, Wrike (Tier 2, task-first tools)**
- These are strong native integrations, not just competitors (all four show up on the /apps/ integrations page)
- Best angle for accounts already committed to one of these: "keep your task tool, add Chanty for the chat and video layer that's missing," rather than a rip-and-replace pitch
- For accounts without a task tool yet: Chanty replaces both at once for less than most of these charge for task management alone

**vs. Basecamp (Tier 2)**
- Both lean into flat, simple pricing and an all-in-one pitch
- Chanty's differentiator is native real-time chat and calls, which Basecamp doesn't have

**vs. Notion (Tier 2)**
- Not a real head-to-head. Notion is docs/wiki, Chanty is real-time comms plus lightweight task tracking
- Likely to surface as an objection ("we already have Notion for this") rather than a true competitive loss — reframe as complementary, not competitive

---

## 6. Objection handling

| Objection | Response angle |
|---|---|
| "We already have Slack" | Price (half the cost), unlimited history on free, native tasks so you can drop a second tool too |
| "We're a Microsoft shop" | No M365 dependency needed, HIPAA/BAA and 2FA/SSO included at Business tier, lighter onboarding |
| "Too small a team to bother" | Free plan supports up to 5 people with unlimited history and calls, not a stripped trial |
| "Compliance is a blocker" (healthcare, finance) | HIPAA/BAA ships on Business ($3/user), not locked to Enterprise like most competitors |
| "Worried about migration/history loss" | Native import tooling from Slack, Teams, and other messengers |
| "We already use [Asana/Monday/ClickUp] for tasks" | Position as additive, not a replacement — Chanty adds the chat/video layer via native integration |

---

## 7. Guardrails for the copy pipeline

- Treat all Chanty-reported stats (75,000 companies, 40% faster response times, 55% more productive, etc.) as Chanty's own claims. Fine to cite in outbound, not something to present as third-party verified.
- The Slack and MS Teams data-ownership comparisons ("we do not sell your data," "we do not train AI on your messages") are sourced directly to Chanty's own healthcare page. Safe to use verbatim. Don't extend them into claims Chanty hasn't made itself (e.g., don't invent specifics about what Slack or MS Teams actually do with data beyond what's stated).
- HIPAA/BAA is a **Business plan** feature, not Enterprise-only. This gets undersold if copy implies compliance requires the top tier — it doesn't, and that's a real edge over competitors who do gate it that way.
- No stated comparison exists on-site for Google Chat. Any messaging built there is inferred positioning, not sourced from Chanty's own claims, so flag it internally as such.
- Big-name logos (Oracle, NASA, Nike, etc.) almost certainly reflect individual teams inside those orgs, not enterprise-wide deployments. Use as social proof, not as implied enterprise case studies, unless you get a real customer story to back it up.

---

## 8. Source map

| Page | What it contributes |
|---|---|
| chanty.com/ (homepage) | Core positioning, logo social proof, security overview, plan summary |
| /features/ | Full feature list: tasks, Kanban, calls, threads, integrations |
| /pricing/ | Exact pricing, plan-by-plan feature breakdown, FAQ |
| /slack-alternative/ | Direct Slack comparison claims (price, speed, storage, history) |
| /security/ | Full compliance and security architecture detail |
| /solutions/healthcare/ | Healthcare-specific stats, HIPAA detail, data-ownership claims vs. Slack/MS Teams |
| /internal-communications/ | Frontline/deskless workforce stats and positioning |
| /internal-communications-retail/ | Retail-specific version of the internal comms page, same core stats |
| /solutions/marketing/ | Marketing agency positioning, client/guest collaboration angle |
| /apps/ | Full integration list — confirms native connections to Asana, Monday, ClickUp, Wrike, Basecamp, HubSpot, Salesforce, Trello, Jira, GitHub, GitLab, Bitbucket, Zapier, Make, n8n |

**Not yet pulled in detail:** /solutions/it-specialists/, /solutions/logistic-companies/, /solutions/property-managers/, /solutions/realtors/, /solutions/restaurants/, /solutions/coaching/, /solutions/education/, /team-collaboration-software/, /team-communication-software/, /team-productivity-software/, /partners/, /downloads/, blog, help center. These smaller solution pages appear to run the same template as marketing and retail, just with swapped vertical pain points, so the pillars above should transfer with light editing. Worth a follow-up pass once you've got real Chanty customer win data to layer in, since that's the piece you're already waiting on for the non-healthcare verticals.
