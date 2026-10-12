from datetime import datetime

from finbot.analysis.score import ScoreCalculator
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


def _score(transactions):
    matches = WasteDetector().find(transactions)
    return ScoreCalculator().calculate(transactions, matches)


def test_no_expenses_gives_perfect_score():
    score = _score([_tx("Зарплата", 500000)])
    assert score.value == 100
    assert score.level == "excellent"


def test_clean_expenses_give_perfect_score():
    score = _score([_tx("Сільпо", -100000)])
    assert score.value == 100
    assert score.waste_share == 0


def test_casino_lowers_score():
    score = _score([_tx("Сільпо", -100000), _tx("Casino", -100000)])
    assert score.value == 25
    assert score.level == "critical"
    assert score.waste_share == 0.5


def test_score_never_below_zero():
    assert _score([_tx("Casino", -100000)]).value == 0
