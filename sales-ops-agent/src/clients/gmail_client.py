"""
Thin wrapper around the Gmail API. Reads threads, extracts the participants
and message bodies the sync engine needs to classify a conversation's stage.
"""
import base64
import os
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GmailClient:
    def __init__(self, credentials_path: str, token_path: str):
        self.token_path = token_path
        creds = Credentials.from_authorized_user_file(token_path)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as f:
                f.write(creds.to_json())
        self.service = build("gmail", "v1", credentials=creds)

    def list_recent_threads(self, lookback_hours: int = 24) -> list[dict]:
        """Returns threads with any activity in the lookback window."""
        after_ts = int((datetime.utcnow() - timedelta(hours=lookback_hours)).timestamp())
        query = f"after:{after_ts} -in:chats"
        results = self.service.users().threads().list(userId="me", q=query, maxResults=100).execute()
        thread_stubs = results.get("threads", [])
        threads = []
        for stub in thread_stubs:
            full = self.service.users().threads().get(userId="me", id=stub["id"], format="full").execute()
            threads.append(self._parse_thread(full))
        return threads

    def _parse_thread(self, thread: dict) -> dict:
        messages = thread.get("messages", [])
        parsed_messages = []
        participants = set()

        for msg in messages:
            headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
            from_addr = headers.get("from", "")
            to_addr = headers.get("to", "")
            date = headers.get("date", "")
            subject = headers.get("subject", "")
            body = self._extract_body(msg["payload"])

            participants.add(from_addr)
            for addr in to_addr.split(","):
                if addr.strip():
                    participants.add(addr.strip())

            parsed_messages.append({
                "from": from_addr,
                "to": to_addr,
                "date": date,
                "subject": subject,
                "body": body,
                "internal_date_ms": int(msg.get("internalDate", 0)),
            })

        return {
            "thread_id": thread["id"],
            "participants": list(participants),
            "messages": sorted(parsed_messages, key=lambda m: m["internal_date_ms"]),
        }

    def _extract_body(self, payload: dict) -> str:
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data")
                    if data:
                        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            # fall back to first part with any data
            for part in payload["parts"]:
                data = part.get("body", {}).get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            return ""
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        return ""
