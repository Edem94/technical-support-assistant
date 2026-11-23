"""Tests for the per-visitor rate limiter, with a fake clock."""
from types import SimpleNamespace

import pytest

from app import rate_limit
from app.rate_limit import RateLimiter, visitor_id


class Clock:
    now = 1000.0

    def __call__(self):
        return self.now


@pytest.fixture
def clock():
    return Clock()


def test_allows_up_to_the_limit_then_reports_the_wait(clock):
    limiter = RateLimiter([(2, 60)], clock)
    assert limiter.check("a") == 0
    clock.now += 20
    assert limiter.check("a") == 0
    clock.now += 10
    assert limiter.check("a") == 30  # the first visit expires 60 s after it happened
    assert limiter.check("b") == 0


def test_window_slides_and_refusals_do_not_extend_it(clock):
    limiter = RateLimiter([(1, 60)], clock)
    assert limiter.check("a") == 0
    clock.now += 59
    assert limiter.check("a") == 1
    clock.now += 1
    assert limiter.check("a") == 0


def test_every_limit_applies(clock):
    limiter = RateLimiter([(2, 60), (3, 86400)], clock)
    for _ in range(3):
        assert limiter.check("a") == 0
        clock.now += 61
    assert limiter.check("a") == 86400 - 3 * 61


def test_number_of_visitors_is_bounded(clock, monkeypatch):
    monkeypatch.setattr(rate_limit, "MAX_VISITORS", 3)
    limiter = RateLimiter([(1, 60)], clock)
    for visitor in "abcd":
        limiter.check(visitor)
    assert list(limiter._visits) == ["b", "c", "d"]


@pytest.mark.parametrize(
    ("forwarded", "hops", "expected"),
    [
        (None, 0, "10.0.0.5"),
        ("203.0.113.1", 0, "10.0.0.5"),  # no trusted proxy: the header is not believed
        ("203.0.113.1", 1, "203.0.113.1"),
        ("1.2.3.4, 203.0.113.1", 1, "203.0.113.1"),
        ("1.2.3.4, 203.0.113.1, 10.1.1.1", 2, "203.0.113.1"),
        (None, 1, "10.0.0.5"),
        ("2001:db8:1:2:aaaa::1", 1, "2001:db8:1:2::/64"),
        ("not-an-address", 1, "not-an-address"),
    ],
)
def test_visitor_id(forwarded, hops, expected):
    headers = {"x-forwarded-for": forwarded} if forwarded else {}
    request = SimpleNamespace(client=SimpleNamespace(host="10.0.0.5"), headers=headers)
    assert visitor_id(request, hops) == expected
