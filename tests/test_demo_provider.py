import asyncio

from finbot.banking.demo import DemoBankingProvider


def test_demo_returns_transactions():
    result = asyncio.run(DemoBankingProvider().get_transactions(30))
    assert len(result) == 17


def test_demo_sorted_newest_first():
    result = asyncio.run(DemoBankingProvider().get_transactions(30))
    times = [t.time for t in result]
    assert times == sorted(times, reverse=True)


def test_demo_respects_days_limit():
    result = asyncio.run(DemoBankingProvider().get_transactions(3))
    assert len(result) < 17
