"""Демонстраційний провайдер: працює без реального банку."""

from datetime import datetime, timedelta

from finbot.banking.base import BankingProvider
from finbot.domain.models import Transaction

# (опис, сума в копійках, категорія, днів тому)
_DEMO_DATA = [
    ("Сільпо", -45620, "Продукти", 1),
    ("АТБ", -31890, "Продукти", 3),
    ("Uber", -18500, "Транспорт", 2),
    ("Метро", -2000, "Транспорт", 4),
    ("Netflix", -29900, "Розваги", 5),
    ("Кінотеатр", -35000, "Розваги", 8),
    ("Аптека", -21700, "Здоровя", 6),
    ("Київстар", -25000, "Звязок", 10),
    ("Кафе", -48000, "Кафе і ресторани", 7),
    ("Ресторан", -125000, "Кафе і ресторани", 12),
    ("Зарплата", 4500000, "Дохід", 15),
    ("Переказ від друга", 150000, "Дохід", 9),
    ("Pin-Up Casino", -150000, "Азартні ігри", 2),
    ("Parimatch ставки", -80000, "Азартні ігри", 6),
    ("OnlyFans підписка", -60000, "Для дорослих", 4),
    ("Лотерея квиток", -10000, "Лотереї", 11),
    ("Таролог онлайн", -35000, "Езотерика", 13),
]


class DemoBankingProvider(BankingProvider):
    async def get_transactions(self, days: int = 30) -> list[Transaction]:
        now = datetime.now()
        result = [
            Transaction(
                id=f"demo-{index}",
                time=now - timedelta(days=days_ago),
                description=description,
                amount_kopecks=amount,
                category=category,
            )
            for index, (description, amount, category, days_ago) in enumerate(_DEMO_DATA)
            if days_ago <= days
        ]
        return sorted(result, key=lambda t: t.time, reverse=True)