
import asyncio

from finbot.llm.risk_classifier import RiskClassifier


async def main():

    classifier = RiskClassifier()

    transactions = [
        {
            "description": "Cosmolot payment",
            "url": "https://cosmolot.ua",
            "amount": 800,
        },
        {
            "description": "Netflix subscription",
            "url": "https://netflix.com",
            "amount": 300,
        },
        {
            "description": "Unknown shop",
            "url": "https://unknown-shop.example",
            "amount": 500,
        },
    ]

    for transaction in transactions:
        print("\nТранзакція:", transaction["description"])

        result = await classifier.classify(transaction)

        print("Категорія:", result["category"])
        print("Ризик:", result["risk_level"])
        print("Причина:", result["reason"])
        print("Рекомендація:", result["recommendation"])

        if "Cosmolot" in transaction["description"]:
            assert result["category"] == "gambling"
            assert result["risk_level"] == "high"

        if "Netflix" in transaction["description"]:
            assert result["category"] == "trusted"
            assert result["risk_level"] == "none"

        if "Unknown" in transaction["description"]:
            assert result["category"] == "unknown"
            assert result["risk_level"] == "unknown"

    print("\nУсі перевірки класифікатора пройдено.")


if __name__ == "__main__":
    asyncio.run(main())
