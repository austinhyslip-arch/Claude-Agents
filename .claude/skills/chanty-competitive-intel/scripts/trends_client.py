"""Google Trends interest-over-time, via the unofficial pytrends library.

pytrends calls the same backend endpoints that power trends.google.com/explore. It is
unofficial: Google changes those endpoints without notice, and rate-limits hard (HTTP 429)
if you query too fast. Two consequences are baked into this module:

  * Every call is wrapped. A failure returns a `TrendResult` with `ok=False` and a reason
    string — it never raises into the digest build. One dead row beats a dead digest.
  * Consecutive failures trip a circuit breaker. When the endpoint is rate-limited or the
    host is blocked outright, every term fails the same way, and retrying 29 of them with
    exponential backoff turns a three-minute run into a half-hour one for no new
    information. After three in a row the source is given up on for the run and the
    remaining rows say so immediately.
  * Calls are serialised with a delay between them, one term per request. Batching five
    keywords per payload would cut the request count, but pytrends normalises a batch's
    index against the batch's own peak, so a batch whose composition changes between weeks
    would silently rescale every value in it. One term per request keeps the index
    comparable week over week.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

DEFAULT_DELAY = 4.0          # seconds between successful requests
DEFAULT_MAX_RETRIES = 3      # attempts per term, including the first
DEFAULT_BACKOFF = 8.0        # seconds; doubles per retry, plus jitter
DEFAULT_FAILURE_LIMIT = 3    # consecutive dead terms before the source is given up on
UP_THRESHOLD = 10.0          # percent change that counts as a real move
DOWN_THRESHOLD = -10.0


@dataclass
class TrendResult:
    query: str
    ok: bool = False
    reason: str = ""
    latest: float | None = None          # most recent complete index point, 0-100
    recent_mean: float | None = None     # mean of the last 14 days
    prior_mean: float | None = None      # mean of the 14 days before that
    delta_pct: float | None = None
    basis: str = ""                      # "week-over-week" or "prior-period"
    arrow: str = "unavailable"           # up | flat | down | unavailable
    series: list[dict] = field(default_factory=list)


def _classify(delta_pct: float | None) -> str:
    if delta_pct is None:
        return "unavailable"
    if delta_pct >= UP_THRESHOLD:
        return "up"
    if delta_pct <= DOWN_THRESHOLD:
        return "down"
    return "flat"


def _pct(new: float | None, old: float | None) -> float | None:
    if new is None or old is None or old <= 0:
        return None
    return round((new - old) / old * 100.0, 1)


class TrendsClient:
    """Thin, failure-tolerant wrapper over pytrends.

    `fetch_series` is the only network call. It is a separate method so the self-test can
    substitute a fake and exercise the whole pipeline offline.
    """

    def __init__(
        self,
        geo: str = "US",
        timeframe: str = "today 3-m",
        hl: str = "en-US",
        tz: int = 360,
        delay: float = DEFAULT_DELAY,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff: float = DEFAULT_BACKOFF,
        failure_limit: int = DEFAULT_FAILURE_LIMIT,
    ) -> None:
        self.geo = geo
        self.timeframe = timeframe
        self.hl = hl
        self.tz = tz
        self.delay = delay
        self.max_retries = max_retries
        self.backoff = backoff
        self.failure_limit = failure_limit
        self._pytrends = None
        self._dead = ""  # set once the source is unusable; skip the rest of the run
        self._consecutive_failures = 0

    @property
    def dead(self) -> str:
        """Non-empty once the source has been given up on for this run."""
        return self._dead

    def _failed(self, reason: str) -> str:
        """Record a failure and trip the breaker if this is the third in a row."""
        self._consecutive_failures += 1
        if self._consecutive_failures >= self.failure_limit:
            self._dead = (f"Google Trends unreachable for this run "
                          f"({self._consecutive_failures} terms failed): {reason}")
        return reason

    def _client(self):
        if self._pytrends is None:
            from pytrends.request import TrendReq  # imported late: optional dependency

            self._pytrends = TrendReq(hl=self.hl, tz=self.tz)
        return self._pytrends

    def fetch_series(self, query: str) -> list[dict]:
        """Return [{"date": "YYYY-MM-DD", "value": float, "partial": bool}, ...]."""
        pytrends = self._client()
        pytrends.build_payload(kw_list=[query], geo=self.geo, timeframe=self.timeframe)
        frame = pytrends.interest_over_time()
        if frame is None or frame.empty or query not in frame:
            return []
        return [
            {
                "date": index.strftime("%Y-%m-%d"),
                "value": float(row[query]),
                "partial": bool(row.get("isPartial", False)),
            }
            for index, row in frame.iterrows()
        ]

    def interest(self, query: str, previous_latest: float | None = None) -> TrendResult:
        """One term's trend, never raising. `previous_latest` is last week's cached index."""
        result = TrendResult(query=query)
        if self._dead:
            result.reason = self._dead
            return result

        last_error = ""
        for attempt in range(1, self.max_retries + 1):
            try:
                series = self.fetch_series(query)
            except ImportError:
                self._dead = "pytrends is not installed"
                result.reason = self._dead
                return result
            except Exception as exc:  # noqa: BLE001 - pytrends raises a wide variety
                last_error = f"{type(exc).__name__}: {exc}".strip()[:200]
                if attempt < self.max_retries:
                    time.sleep(self.backoff * (2 ** (attempt - 1)) + random.uniform(0, 2))
                    continue
                result.reason = self._failed(last_error)
                return result

            if not series:
                # A term Google has no data for is not a broken source — it says nothing
                # about the next term, so it does not count toward the breaker.
                self._consecutive_failures = 0
                result.reason = "no data returned for this term"
                return result

            self._consecutive_failures = 0
            complete = [p for p in series if not p["partial"]] or series
            values = [p["value"] for p in complete]
            result.ok = True
            result.series = complete[-28:]
            result.latest = values[-1]
            result.recent_mean = round(sum(values[-14:]) / len(values[-14:]), 1)
            older = values[-28:-14]
            result.prior_mean = round(sum(older) / len(older), 1) if older else None

            wow = _pct(result.latest, previous_latest)
            if wow is not None:
                result.delta_pct, result.basis = wow, "week-over-week"
            else:
                result.delta_pct = _pct(result.recent_mean, result.prior_mean)
                result.basis = "prior-period" if result.delta_pct is not None else ""
            result.arrow = _classify(result.delta_pct)
            return result

        result.reason = self._failed(last_error or "unknown failure")
        return result

    def sleep_between(self) -> None:
        """Called by the caller between terms. Jittered so the cadence isn't a metronome."""
        time.sleep(self.delay + random.uniform(0, 1.5))
