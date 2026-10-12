from datetime import datetime

from finbot.analysis.waste_detector import WasteDetector
from finbot.domain.models import Transaction


def _tx(description: str, amount_kopecks: int) -> Transaction:
    return Transaction(
        id="t",
        time=datetime(2026, 10, 1),
        description=description,
        amount_kopecks=amount_kopecks,
        category="Тест",
    )


def test_finds_casino():
    matches = WasteDetector().find([_tx("Pin-Up Casino", -100000)])
    assert len(matches) == 1
    assert matches[0].category.key == "gambling"


def test_search_is_case_insensitive():
    assert len(WasteDetector().find([_tx("PARIMATCH", -5000)])) == 1


def test_ignores_normal_expenses():
    assert WasteDetector().find([_tx("Сільпо", -45000)]) == []


def test_ignores_income_even_with_keyword():
    assert WasteDetector().find([_tx("casino виграш", 100000)]) == []


def test_each_transaction_matches_once():
    assert len(WasteDetector().find([_tx("casino lottery", -1000)])) == 1
