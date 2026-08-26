"""SERP snapshots from the Google Custom Search JSON API.

This is the official API and the reliable half of the build: it answers "who ranks for
`slack alternatives` right now", which is the direct input for content-gap ideas. It is
also the same API the social-listening work already uses, so the credentials are shared.

Credentials come from the environment:
  GOOGLE_CSE_API_KEY  — API key
  GOOGLE_CSE_CX       — search engine id, configured to search the entire web

Quota note: the free tier is 100 queries/day. A full weekly run is one query per term.
"""

from __future__ import annotations

import os
import random
import time
import urllib.parse
from dataclasses import dataclass, field

ENDPOINT = "https://www.googleapis.com/customsearch/v1"
DEFAULT_DELAY = 1.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF = 4.0


@dataclass
class SerpResult:
    query: str
    ok: bool = False
    reason: str = ""
    results: list[dict] = field(default_factory=list)  # [{rank, domain, title, link}]

    @property
    def domains(self) -> list[str]:
        return [r["domain"] for r in self.results]

    def top(self, n: int = 3) -> list[str]:
        return self.domains[:n]

    def rank_of(self, domains: list[str]) -> int | None:
        """1-based rank of the first result on any of `domains`, or None."""
        wanted = {d.lower().lstrip("www.") for d in domains}
        for r in self.results:
            if r["domain"].lower().lstrip("www.") in wanted:
                return r["rank"]
        return None


def domain_of(link: str) -> str:
    host = urllib.parse.urlsplit(link).netloc.lower()
    return host[4:] if host.startswith("www.") else host


class SerpClient:
    def __init__(
        self,
        api_key: str | None = None,
        cx: str | None = None,
        depth: int = 10,
        delay: float = DEFAULT_DELAY,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff: float = DEFAULT_BACKOFF,
        geo: str = "US",
    ) -> None:
        self.api_key = api_key or os.environ.get("GOOGLE_CSE_API_KEY", "")
        self.cx = cx or os.environ.get("GOOGLE_CSE_CX", "")
        self.depth = min(depth, 10)  # one API page; 10 is the per-request maximum
        self.delay = delay
        self.max_retries = max_retries
        self.backoff = backoff
        self.geo = geo

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.cx)

    def fetch(self, query: str) -> list[dict]:
        """Raw API call. Overridden in the self-test to run the pipeline offline."""
        import requests  # imported late so the module imports without the dependency

        response = requests.get(
            ENDPOINT,
            params={
                "key": self.api_key,
                "cx": self.cx,
                "q": query,
                "num": self.depth,
                "gl": self.geo.lower(),
                "hl": "en",
            },
            timeout=30,
        )
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text[:160]}")
        return response.json().get("items", []) or []

    def search(self, query: str) -> SerpResult:
        """One term's SERP, never raising."""
        result = SerpResult(query=query)
        if not self.configured:
            result.reason = "GOOGLE_CSE_API_KEY / GOOGLE_CSE_CX not set"
            return result

        last_error = ""
        for attempt in range(1, self.max_retries + 1):
            try:
                items = self.fetch(query)
            except Exception as exc:  # noqa: BLE001
                last_error = f"{type(exc).__name__}: {exc}".strip()[:200]
                if attempt < self.max_retries:
                    time.sleep(self.backoff * (2 ** (attempt - 1)) + random.uniform(0, 1))
                    continue
                result.reason = last_error
                return result

            result.ok = True
            result.results = [
                {
                    "rank": i,
                    "domain": domain_of(item.get("link", "")),
                    "title": (item.get("title") or "")[:160],
                    "link": item.get("link", ""),
                }
                for i, item in enumerate(items[: self.depth], start=1)
                if item.get("link")
            ]
            if not result.results:
                result.reason = "no results returned"
            return result

        result.reason = last_error or "unknown failure"
        return result

    def sleep_between(self) -> None:
        time.sleep(self.delay + random.uniform(0, 0.5))
