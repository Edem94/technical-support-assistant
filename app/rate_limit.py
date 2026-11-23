"""Per-visitor rate limiting for POST /ask, because every question is a paid Claude call.

Counts are kept in memory, so each server process has its own and a restart clears them.
"""
import ipaddress
import math
import threading
import time
from collections import OrderedDict, deque
from collections.abc import Callable

from fastapi import Request

MAX_VISITORS = 10_000  # Oldest visitors are forgotten beyond this, so memory stays bounded.


class RateLimiter:
    """Sliding windows: a visitor must be under every (limit, window in seconds) pair."""

    def __init__(self, limits: list[tuple[int, float]], clock: Callable[[], float] = time.monotonic):
        self.limits = limits
        self.clock = clock
        self._visits: OrderedDict[str, deque[float]] = OrderedDict()
        self._lock = threading.Lock()  # /ask runs in several threads

    def check(self, visitor: str) -> int:
        """Record a request and return 0, or return the seconds to wait if it is over a limit.

        Refused requests are not recorded, so retrying early does not extend the wait.
        """
        with self._lock:
            now = self.clock()
            visits = self._visits.setdefault(visitor, deque())
            self._visits.move_to_end(visitor)
            while len(self._visits) > MAX_VISITORS:
                self._visits.popitem(last=False)

            longest = max(window for _, window in self.limits)
            while visits and visits[0] <= now - longest:
                visits.popleft()

            wait = 0.0
            for limit, window in self.limits:
                if len(visits) >= limit:
                    # The request becomes allowed once the limit-th most recent visit expires.
                    wait = max(wait, visits[-limit] + window - now)
            if wait > 0:
                return math.ceil(wait)
            visits.append(now)
            return 0


def visitor_id(request: Request, trusted_proxy_hops: int) -> str:
    """The visitor's address. Behind proxies it comes from X-Forwarded-For.

    Each proxy appends the address it saw, so only the last `trusted_proxy_hops` entries can be
    believed; anything before them is whatever the visitor sent, and could be made up.
    """
    address = request.client.host if request.client else "unknown"
    if trusted_proxy_hops:
        forwarded = [part.strip() for part in request.headers.get("x-forwarded-for", "").split(",")]
        if len(forwarded) >= trusted_proxy_hops and forwarded[-trusted_proxy_hops]:
            address = forwarded[-trusted_proxy_hops]
    try:
        parsed = ipaddress.ip_address(address)
    except ValueError:
        return address
    if parsed.version == 6:  # One visitor usually has a whole /64 to pick addresses from.
        return str(ipaddress.ip_network((parsed, 64), strict=False))
    return address
