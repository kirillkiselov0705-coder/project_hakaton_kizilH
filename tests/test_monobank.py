import asyncio

import httpx
import pytest

from finbot.banking.monobank import (
    InvalidTokenError,
    MonobankProvider,
    RateLimitError,
)

STATEMENT = [
    {"id": "1", "time": 1760000000, "description": "Сільпо", "amount": -10000, "mcc": 5411},
    {"id": "2", "time": 1760100000, "description": "Зарплата", "amount": 500000, "mcc": 4829},
]


def _run(handler, action):
    async def runner():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as http:
            provider = MonobankProvider("test-token", http)
            return await action(provider)

    return asyncio.run(runner())


def test_parses_transactions():
    result = _run(lambda r: httpx.Response(200, json=STATEMENT), lambda p: p.get_transactions(30))
    assert len(result) == 2
    assert result[0].description == "Сільпо"
    assert result[0].amount == -100.0
    assert result[0].is_expense is True


def test_sends_token_header():
    seen = {}

    def handler(request):
        seen["token"] = request.headers.get("X-Token")
        return httpx.Response(200, json=[])

    _run(handler, lambda p: p.get_transactions(30))
    assert seen["token"] == "test-token"


def test_invalid_token_raises():
    with pytest.raises(InvalidTokenError):
        _run(lambda r: httpx.Response(403, json={}), lambda p: p.check_token())


def test_rate_limit_raises():
    with pytest.raises(RateLimitError):
        _run(lambda r: httpx.Response(429, json={}), lambda p: p.get_transactions(30))


def test_second_call_uses_cache():
    calls = {"count": 0}

    def handler(request):
        calls["count"] += 1
        return httpx.Response(200, json=STATEMENT)

    async def action(provider):
        await provider.get_transactions(30)
        await provider.get_transactions(30)

    _run(handler, action)
    assert calls["count"] == 1
