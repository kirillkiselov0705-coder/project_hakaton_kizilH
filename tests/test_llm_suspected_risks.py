
import asyncio

from finbot.llm.financial_service import FinancialService


async def main():
    service = FinancialService()

    transactions = [
        {
            "description": "Super Spin Casino deposit",
            "url": "https://super-spin.example",
            "mcc": 7995,
            "amount": 500,
            "category": "Розваги",
        },
        {
            "description": "Premium adult video subscription",
            "url": "https://adult-premium.example",
            "amount": 250,
            "category": "Підписки",
        },
        {
            "description": "Local grocery store",
            "url": "https://grocery-example.test",
            "amount": 1000,
            "category": "Продукти",
        },
    ]

    result = await service.analyze(transactions)

    print("Загальні витрати:", result["total"])
    print("Оцінка:", result["score"])
    print("Підтверджені ризики:",
          len(result["confirmed_risks"]))
    print("Ймовірні ризики:",
          len(result["suspected_risks"]))

    assert result["total"] == 1750
    assert result["score"] == 10
    assert len(result["confirmed_risks"]) == 0
    assert len(result["suspected_risks"]) == 2

    print("Усі перевірки пройдено успішно.")


if __name__ == "__main__":
    asyncio.run(main())
