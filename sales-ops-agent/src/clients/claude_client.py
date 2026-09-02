"""
Uses the Anthropic API to read an email thread and decide what pipeline
stage the conversation is in, plus whether a follow-up is needed.
"""
import json

from anthropic import Anthropic

STAGE_CLASSIFICATION_PROMPT = """You're reviewing an email thread between Austin (co-founder of Chanty, \
a HIPAA-compliant team chat tool for small healthcare clinics) and a prospect from cold outreach. Based \
on the thread, classify it into Austin's actual Attio pipeline stage.

Valid stages, in pipeline order:
- Not Contacted: no outreach sent yet (shouldn't apply to a thread that exists, included for completeness)
- Contacted: initial cold email sent, no reply yet
- Follow-Up Sent: at least one follow-up has gone out, still no reply
- Replied: the prospect has responded at least once, no meeting booked yet
- Meeting Booked: a meeting has been proposed and a specific time confirmed in the thread
- Opportunity: active conversation about pricing, a demo happened, or real buying interest is clear
- Contracting: contract or legal terms being discussed
- WON-Closed: they signed / became a customer
- LOST-Closed: they explicitly declined or the deal is dead
- Not a Fit: they replied but are disqualified (wrong size clinic, already have a tool, etc.)
- Follow Up Needed: explicit ambiguous catch-all, use only if nothing else fits

Also flag delivery failures (bounces, spam blocks) distinctly, those aren't a stage, they mean the outreach \
never reached the person.

Thread participants: {participants}

Thread messages (oldest first):
{thread_text}

Respond with ONLY valid JSON, no other text, in this exact shape:
{{
  "stage": "one of the valid stages above, or null if this is a bounce/delivery failure with no real contact",
  "is_bounce_or_failure": true or false,
  "prospect_replied": true or false,
  "meeting_mentioned": true or false,
  "meeting_confirmed_in_thread": true or false,
  "needs_followup": true or false,
  "followup_reason": "short phrase, e.g. 'no reply to initial outreach' or 'proposal sent awaiting response'",
  "confidence": "high, medium, or low"
}}
"""


class ClaudeClient:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def classify_thread(self, thread: dict, stage_values: list[str]) -> dict:
        thread_text = "\n\n---\n\n".join(
            f"From: {m['from']}\nTo: {m['to']}\nDate: {m['date']}\nSubject: {m['subject']}\n\n{m['body'][:2000]}"
            for m in thread["messages"]
        )
        prompt = STAGE_CLASSIFICATION_PROMPT.format(
            participants=", ".join(thread["participants"]),
            thread_text=thread_text,
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()
        # strip markdown fences if the model adds them despite instructions
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "stage": None,
                "needs_followup": False,
                "followup_reason": "classification_failed",
                "confidence": "low",
                "raw_response": text,
            }
