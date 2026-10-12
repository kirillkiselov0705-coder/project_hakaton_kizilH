"""Доменні моделі. Не залежать від зовнішніх бібліотек."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    """Одна банківська транзакція.

    Сума в копійках: від'ємна для витрат, додатна для надходжень.
    """

    id: str
    time: datetime
    description: str
    amount_kopecks: int
    category: str

    @property
    def amount(self) -> float:
        return self.amount_kopecks / 100

    @property
    def is_expense(self) -> bool:
        return self.amount_kopecks < 0