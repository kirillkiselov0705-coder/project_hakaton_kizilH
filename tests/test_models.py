from datetime import datetime

from finbot.domain.models import Transaction


def _tx(amount_kopecks: int) -> Transaction:
    return Transaction(
        id="t1",
        time=datetime(2026, 10, 1),
        description="Тест",
        amount_kopecks=amount_kopecks,
        category="Тест",
    )


def test_amount_converts_kopecks_to_hryvnia():
    assert _tx(-45620).amount == -456.20


def test_expense_is_negative():
    assert _tx(-100).is_expense is True


def test_income_is_not_expense():
    assert _tx(100).is_expense is False
