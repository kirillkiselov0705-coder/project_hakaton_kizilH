"""Вибір джерела банківських даних для кожного користувача."""

import httpx

from finbot.banking.base import BankingProvider
from finbot.banking.demo import DemoBankingProvider
from finbot.banking.monobank import MonobankProvider


class BankingResolver:
    def __init__(self, http: httpx.AsyncClient, demo_mode: bool) -> None:
        self._http = http
        self._demo = DemoBankingProvider() if demo_mode else None
        self._users: dict[int, MonobankProvider] = {}

    async def connect(self, user_id: int, token: str) -> None:
        """Перевіряє токен і підключає користувача. Кидає MonobankError."""
        provider = MonobankProvider(token, self._http)
        await provider.check_token()
        self._users[user_id] = provider

    def disconnect(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None

    def is_connected(self, user_id: int) -> bool:
        return user_id in self._users

    def for_user(self, user_id: int) -> BankingProvider | None:
        return self._users.get(user_id) or self._demo