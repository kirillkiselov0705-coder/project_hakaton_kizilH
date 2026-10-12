
import asyncio

from finbot.llm.financial_service import FinancialService


async def main():

    service = FinancialService()

    transactions = [
        {
            "description": "Cosmolot",
            "url": "https://cosmolot.ua",
            "amount": 800,
            "category": "Розваги",
        },
        {
            "description": "Netflix",
            "url": "https://netflix.com",
            "amount": 300,
            "category": "Підписки",
        },
        {
            "description": "АТБ",
            "url": "https://atbmarket.com",
            "amount": 1200,
            "category": "Продукти",
        },
    ]

    result = await service.analyze(transactions)

    print("Загальні витрати:", result["total"])
    print("Оцінка:", result["score"], "/10")
    print("Підозрілі операції:", len(result["suspicious"]))

    for transaction in result["transactions"]:
        print(
            transaction["description"],
            "->",
            transaction["risk_category"],
        )

    assert result["total"] == 2300
    assert result["score"] == 5
    assert len(result["suspicious"]) == 1
    assert result["suspicious"][0]["description"] == "Cosmolot"

    print("\nУсі перевірки пройдено успішно.")


if __name__ == "__main__":
    asyncio.run(main())
