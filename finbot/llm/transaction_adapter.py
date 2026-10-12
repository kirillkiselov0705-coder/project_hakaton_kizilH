
from finbot.domain.models import Transaction


class TransactionAdapter:

    @staticmethod
    def convert(transactions: list[Transaction]) -> list[dict]:
        result = []

        for transaction in transactions:
            if not transaction.is_expense:
                continue

            result.append({
                "description": transaction.description,
                "amount": abs(transaction.amount_kopecks) / 100,
                "category": transaction.category,
                "url": "",
            })

        return result
