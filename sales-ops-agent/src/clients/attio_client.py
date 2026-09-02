"""
Thin wrapper around the Attio REST API. Finds people records by email and
updates their stage / last-contacted fields.

Docs: https://developers.attio.com
"""
import requests


class AttioClient:
    BASE_URL = "https://api.attio.com/v2"

    def __init__(self, api_key: str, stage_slug: str = "stage", last_contacted_slug: str = "last_contacted_at"):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.stage_slug = stage_slug
        self.last_contacted_slug = last_contacted_slug

    def find_person_by_email(self, email: str) -> dict | None:
        url = f"{self.BASE_URL}/objects/people/records/query"
        body = {
            "filter": {"email_addresses": {"$contains": email}},
            "limit": 1,
        }
        resp = requests.post(url, headers=self.headers, json=body)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return data[0] if data else None

    def stage_attribute_exists(self) -> bool:
        url = f"{self.BASE_URL}/objects/people/attributes"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        slugs = [a["api_slug"] for a in resp.json().get("data", [])]
        return self.stage_slug in slugs

    def update_stage(self, record_id: str, stage_value: str, last_contacted_iso: str, dry_run: bool = True) -> dict:
        if dry_run:
            return {"dry_run": True, "record_id": record_id, "would_set_stage": stage_value,
                     "would_set_last_contacted": last_contacted_iso}

        url = f"{self.BASE_URL}/objects/people/records/{record_id}"
        body = {
            "data": {
                "values": {
                    self.stage_slug: stage_value,
                    self.last_contacted_slug: last_contacted_iso,
                }
            }
        }
        resp = requests.patch(url, headers=self.headers, json=body)
        resp.raise_for_status()
        return resp.json()

    def create_person(self, email: str, name: str, dry_run: bool = True) -> dict:
        if dry_run:
            return {"dry_run": True, "would_create": email}

        url = f"{self.BASE_URL}/objects/people/records"
        body = {
            "data": {
                "values": {
                    "email_addresses": [email],
                    "name": name,
                }
            }
        }
        resp = requests.post(url, headers=self.headers, json=body)
        resp.raise_for_status()
        return resp.json()
