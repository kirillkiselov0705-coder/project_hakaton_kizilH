"""Клієнт monobank (персональний API, лише читання)."""

import time
from datetime import datetime

import httpx

from finbot.banking.base import BankingProvider
from finbot.domain.models import Transaction

API_URL = "https://api.monobank.ua"
MAX_DAYS = 31
CACHE_SECONDS = 60  # monobank дозволяє 1 запит виписки на 60 секунд


class MonobankError(Exception):
    """Загальна помилка monobank."""


class InvalidTokenError(MonobankError):
    """Токен недійсний."""


class RateLimitError(MonobankError):
    """Занадто часті запити."""


class MonobankProvider(BankingProvider):
    def __init__(self, token: str, http: httpx.AsyncClient) -> None:
        self._token = token
        self._http = http
        self._cache: tuple[float, int, list[Transaction]] | None = None

    async def _get(self, path: str) -> list | dict:
        response = await self._http.get(
            f"{API_URL}{path}", headers={"X-Token": self._token}
        )
        if response.status_code in (401, 403):
            raise InvalidTokenError
        if response.status_code == 429:
            raise RateLimitError
        response.raise_for_status()
        return response.json()

    async def check_token(self) -> None:
        await self._get("/personal/client-info")

    async def get_transactions(self, days: int = 30) -> list[Transaction]:
        days = min(days, MAX_DAYS)
        now = time.time()
        if self._cache and now - self._cache[0] < CACHE_SECONDS and self._cache[1] == days:
            return self._cache[2]

        date_to = int(now)
        date_from = date_to - days * 86400
        items = await self._get(f"/personal/statement/0/{date_from}/{date_to}")
        result = [
            Transaction(
                id=item["id"],
                time=datetime.fromtimestamp(item["time"]),
                description=item.get("description", ""),
                amount_kopecks=item["amount"],
                category=f"MCC {item.get('mcc', '')}",
            )
            for item in items
        ]
        self._cache = (now, days, result)
        return result