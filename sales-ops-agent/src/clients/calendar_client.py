"""
Thin wrapper around the Google Calendar API. Checks whether meetings mentioned
in email actually got booked, and creates follow-up hold events.
"""
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class CalendarClient:
    def __init__(self, token_path: str, timezone: str = "America/Chicago"):
        creds = Credentials.from_authorized_user_file(token_path)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as f:
                f.write(creds.to_json())
        self.service = build("calendar", "v3", credentials=creds)
        self.timezone = timezone

    def list_upcoming_events(self, days_ahead: int = 14) -> list[dict]:
        now = datetime.utcnow().isoformat() + "Z"
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"
        result = self.service.events().list(
            calendarId="primary", timeMin=now, timeMax=end,
            singleEvents=True, orderBy="startTime", maxResults=250,
        ).execute()
        return result.get("items", [])

    def find_event_with_attendee(self, email: str, days_ahead: int = 14) -> dict | None:
        events = self.list_upcoming_events(days_ahead=days_ahead)
        for event in events:
            attendees = event.get("attendees", [])
            for attendee in attendees:
                if attendee.get("email", "").lower() == email.lower():
                    return event
        return None

    def create_followup_hold(self, contact_name: str, contact_email: str, when: datetime, notes: str = "") -> dict:
        """Creates a private hold on Austin's own calendar. Does not invite the contact."""
        event = {
            "summary": f"Follow up: {contact_name}",
            "description": f"Auto-scheduled by sales ops agent.\nContact: {contact_email}\n{notes}",
            "start": {"dateTime": when.isoformat(), "timeZone": self.timezone},
            "end": {"dateTime": (when + timedelta(minutes=15)).isoformat(), "timeZone": self.timezone},
            "reminders": {"useDefault": True},
        }
        return self.service.events().insert(calendarId="primary", body=event).execute()
