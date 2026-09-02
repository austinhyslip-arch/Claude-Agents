"""
Entry point. Run daily via cron, GitHub Actions, or a scheduled cloud function.

Usage:
    python src/main.py            # live run, writes to Attio and Calendar
    python src/main.py --dry-run  # logs what it would do, writes nothing
"""
import argparse
import logging
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cadence import load_cadence_rules
from src.clients.attio_client import AttioClient
from src.clients.calendar_client import CalendarClient
from src.clients.claude_client import ClaudeClient
from src.clients.gmail_client import GmailClient
from src.sync_engine import run_sync


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/agent.log"),
            logging.StreamHandler(),
        ],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Log actions without writing to any system")
    args = parser.parse_args()

    load_dotenv()
    setup_logging()
    logger = logging.getLogger("sales_ops_agent")

    required_env = ["ATTIO_API_KEY", "ANTHROPIC_API_KEY", "GMAIL_ACCOUNT"]
    missing = [v for v in required_env if not os.getenv(v)]
    if missing:
        logger.error("Missing required environment variables: %s. Check your .env file.", missing)
        sys.exit(1)

    cadence_rules = load_cadence_rules()

    gmail = GmailClient(
        credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH", "config/google_credentials.json"),
        token_path=os.getenv("GOOGLE_TOKEN_PATH", "config/google_token.json"),
    )
    calendar = CalendarClient(
        token_path=os.getenv("GOOGLE_TOKEN_PATH", "config/google_token.json"),
        timezone=os.getenv("TIMEZONE", "America/Chicago"),
    )
    attio = AttioClient(
        api_key=os.getenv("ATTIO_API_KEY"),
        stage_slug=os.getenv("ATTIO_STAGE_SLUG", "stage"),
        last_contacted_slug=os.getenv("ATTIO_LAST_CONTACTED_SLUG", "last_contacted_at"),
    )
    claude = ClaudeClient(api_key=os.getenv("ANTHROPIC_API_KEY"))

    dry_run = args.dry_run
    logger.info("Starting sales ops agent run. dry_run=%s", dry_run)

    results = run_sync(
        gmail=gmail, attio=attio, claude=claude,
        cadence_rules=cadence_rules, calendar=calendar, dry_run=dry_run,
        gmail_account=os.getenv("GMAIL_ACCOUNT"),
    )

    logger.info("Done. %d threads processed, %d Attio updates, %d follow-ups scheduled, %d bounces skipped.",
                results["threads_processed"], results["attio_updates"],
                results["followups_scheduled"], results["bounces_skipped"])

    if results["errors"]:
        logger.warning("%d threads failed to process, see log above for details.", len(results["errors"]))


if __name__ == "__main__":
    main()
