"""Розрахунок оцінки фінансової дисципліни."""

from dataclasses import dataclass

from finbot.analysis.waste_detector import WasteMatch
from finbot.domain.models import Transaction


@dataclass(frozen=True)
class FinanceScore:
    value: int          # від 0 до 100
    level: str          # excellent, ok, warning, critical
    waste_share: float  # частка порожніх витрат від усіх витрат, 0..1


def _level_for(value: int) -> str:
    if value >= 80:
        return "excellent"
    if value >= 60:
        return "ok"
    if value >= 40:
        return "warning"
    return "critical"


class ScoreCalculator:
    def calculate(
        self, transactions: list[Transaction], matches: list[WasteMatch]
    ) -> FinanceScore:
        total = sum(abs(t.amount) for t in transactions if t.is_expense)
        if total == 0:
            return FinanceScore(value=100, level="excellent", waste_share=0.0)

        waste = sum(abs(m.transaction.amount) for m in matches)
        weighted = sum(abs(m.transaction.amount) * m.category.weight for m in matches)

        value = max(0, min(100, round(100 * (1 - weighted / total))))
        return FinanceScore(
            value=value,
            level=_level_for(value),
            waste_share=min(1.0, waste / total),
        )