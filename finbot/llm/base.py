from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from finbot.domain.models import Transaction


class FinanceAssistant(Protocol):

    async def is_finance_topic(self, text: str) -> bool:
        """Проверяет, относится ли вопрос к финансам."""
        ...

    async def answer(
        self,
        question: str,
        transactions: list["Transaction"],
    ) -> str:
        """Анализирует вопрос и транзакции, возвращает ответ."""
        ...
