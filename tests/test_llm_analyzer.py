
from finbot.llm.analyzer import TransactionAnalyzer


def test_analyzer():
    transactions = [
        {
            "description": "АТБ",
            "amount": 1200,
            "category": "Продукти",
        },
        {
            "description": "Кав'ярня",
            "amount": 450,
            "category": "Кафе",
        },
        {
            "description": "Online Casino",
            "amount": 800,
            "category": "Розваги",
        },
        {
            "description": "Netflix",
            "amount": 300,
            "category": "Підписки",
        },
    ]

    analyzer = TransactionAnalyzer()
    result = analyzer.analyze(transactions)

    assert result["total"] == 2750
    assert result["categories"]["Продукти"] == 1200
    assert len(result["suspicious"]) == 1
    assert result["suspicious"][0]["description"] == "Online Casino"


if __name__ == "__main__":
    test_analyzer()
    print("Усі перевірки пройдено успішно.")
