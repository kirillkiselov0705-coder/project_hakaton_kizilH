"""Пошук «порожніх» витрат у списку транзакцій."""

from dataclasses import dataclass

from finbot.analysis.waste_rules import WASTE_CATEGORIES, WasteCategory
from finbot.domain.models import Transaction


@dataclass(frozen=True)
class WasteMatch:
    transaction: Transaction
    category: WasteCategory


class WasteDetector:
    def __init__(self, categories: tuple[WasteCategory, ...] = WASTE_CATEGORIES) -> None:
        self._categories = categories

    def find(self, transactions: list[Transaction]) -> list[WasteMatch]:
        matches: list[WasteMatch] = []
        for transaction in transactions:
            if not transaction.is_expense:
                continue
            text = transaction.description.lower()
            for category in self._categories:
                if any(keyword in text for keyword in category.keywords):
                    matches.append(WasteMatch(transaction, category))
                    break
        return matches