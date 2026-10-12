
import asyncio

from finbot.llm.risk_classifier import RiskClassifier


async def main():
    classifier = RiskClassifier()

    transactions = [
        {
            "description": "Super Spin Casino deposit",
            "url": "https://super-spin.example",
            "mcc": 7995,
            "amount": 500,
        },
        {
            "description": "Premium adult video subscription",
            "url": "https://adult-premium.example",
            "amount": 250,
        },
        {
            "description": "Local grocery store",
            "url": "https://grocery-example.test",
            "amount": 350,
        },
    ]

    for transaction in transactions:
        result = await classifier.classify(transaction)

        print("\nТранзакція:", transaction["description"])
        print("Категорія:", result["category"])
        print("Статус:", result["status"])
        print("Ризик:", result["risk_level"])
        print("Причина:", result["reason"])


if __name__ == "__main__":
    asyncio.run(main())
