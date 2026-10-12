"""Абстракція банківського провайдера."""

from abc import ABC, abstractmethod

from finbot.domain.models import Transaction


class BankingProvider(ABC):
    """Що має вміти будь-яке джерело банківських даних."""

    @abstractmethod
    async def get_transactions(self, days: int = 30) -> list[Transaction]:
        """Повертає транзакції за останні `days` днів, найновіші першими."""