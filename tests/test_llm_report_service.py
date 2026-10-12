
import asyncio

from finbot.llm.report_service import ReportService


async def main():

    service = ReportService()

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

    report = await service.generate(
        "Проаналізуйте мої витрати за місяць",
        transactions,
    )

    print(report)

    assert "2300" in report
    assert "5/10" in report
    assert "Cosmolot" in report

    print("\nЗвіт успішно сформовано.")


if __name__ == "__main__":
    asyncio.run(main())
