"""
The actual daily job. For each recent email thread:
  1. Classify the conversation into Austin's real Attio pipeline stage
  2. Match the contact in Attio, update their stage and last-contacted date
  3. Check the calendar for a meeting mentioned in the thread; flag if it's missing
  4. Schedule a follow-up hold based on the cadence rule for that stage
"""
import logging
from datetime import datetime, timedelta

from src.cadence import days_until_followup

logger = logging.getLogger("sales_ops_agent")


def run_sync(gmail, attio, claude, cadence_rules, calendar=None, dry_run: bool = True, gmail_account: str = ""):
    stage_exists = attio.stage_attribute_exists()
    if not stage_exists:
        logger.warning(
            "Attio has no '%s' status attribute on People yet. Running in "
            "report-only mode: nothing will be written to Attio until that "
            "field exists. See README for setup.", attio.stage_slug
        )

    threads = gmail.list_recent_threads(lookback_hours=24)
    logger.info("Found %d threads with activity in the lookback window.", len(threads))

    results = {"threads_processed": 0, "attio_updates": 0, "followups_scheduled": 0,
               "meetings_flagged_missing": 0, "bounces_skipped": 0, "errors": []}

    for thread in threads:
        try:
            _process_thread(thread, gmail_account, attio, claude, cadence_rules, calendar, dry_run, stage_exists, results)
            results["threads_processed"] += 1
        except Exception as e:
            logger.exception("Failed processing thread %s", thread.get("thread_id"))
            results["errors"].append({"thread_id": thread.get("thread_id"), "error": str(e)})

    logger.info("Run complete: %s", results)
    return results


def _process_thread(thread, gmail_account, attio, claude, cadence_rules, calendar, dry_run, stage_exists, results):
    external_participants = [p for p in thread["participants"] if gmail_account.lower() not in p.lower()]
    if not external_participants:
        return

    contact_email = _extract_email(external_participants[0])
    if not contact_email:
        return

    classification = claude.classify_thread(thread, cadence_rules["stage_values"])
    logger.info("Thread %s classified as: %s", thread["thread_id"], classification)

    if classification.get("is_bounce_or_failure"):
        logger.info("Thread with %s is a bounce/delivery failure, not a real contact. No stage update, no follow-up.", contact_email)
        results["bounces_skipped"] += 1
        return

    if classification.get("confidence") == "low":
        logger.info("Low confidence classification for %s, skipping automated writes, logging only.", contact_email)
        return

    last_message_ts = thread["messages"][-1]["internal_date_ms"] / 1000
    last_contacted_iso = datetime.utcfromtimestamp(last_message_ts).isoformat() + "Z"

    if stage_exists and classification.get("stage"):
        person = attio.find_person_by_email(contact_email)
        if person:
            attio.update_stage(person["id"]["record_id"], classification["stage"], last_contacted_iso, dry_run=dry_run)
            results["attio_updates"] += 1
            logger.info("%s -> stage set to '%s'", contact_email, classification["stage"])
        else:
            logger.info("No Attio record found for %s, skipping update (not auto-creating contacts).", contact_email)

    if calendar is not None and classification.get("meeting_mentioned") and not classification.get("meeting_confirmed_in_thread"):
        existing_event = calendar.find_event_with_attendee(contact_email)
        if not existing_event:
            logger.warning("Meeting mentioned with %s but no calendar event found. Flagging for manual review.", contact_email)
            results["meetings_flagged_missing"] += 1

    if classification.get("needs_followup"):
        days_out = days_until_followup(classification, cadence_rules)
        if days_out is None:
            logger.info("Stage '%s' for %s doesn't call for an auto follow-up, skipping.",
                        classification.get("stage"), contact_email)
            return

        when = datetime.now() + timedelta(days=days_out)
        when = when.replace(hour=9, minute=0, second=0, microsecond=0)

        if calendar is not None:
            if not dry_run:
                calendar.create_followup_hold(
                    contact_name=contact_email.split("@")[0],
                    contact_email=contact_email,
                    when=when,
                    notes=classification.get("followup_reason", ""),
                )
            results["followups_scheduled"] += 1
            logger.info("Follow-up scheduled with %s for %s (%s)",
                        contact_email, when.date(), classification.get("followup_reason"))


def _extract_email(raw_address: str) -> str:
    if "<" in raw_address and ">" in raw_address:
        return raw_address.split("<")[1].split(">")[0].strip()
    return raw_address.strip()
