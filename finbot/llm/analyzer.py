from decimal import Decimal


class TransactionAnalyzer:
    def analyze(self, transactions: list[dict]) -> dict:
        total = Decimal("0")
        categories = {}
        suspicious = []

        risky_words = [
            "casino",
            "казино",
            "gambling",
            "betting",
            "porn",
            "adult",
        ]

        for transaction in transactions:
            description = str(
                transaction.get("description", "")
            ).lower()

            amount = Decimal(str(transaction["amount"]))

            # В демонстраційних даних витрати додатні.
            # Реальний monobank використовує від'ємні
            # суми для списань і копійки замість гривень.
            if amount <= 0:
                continue

            category = transaction.get(
                "category", "Інше"
            )

            total += amount

            categories[category] = (
                categories.get(category, Decimal("0"))
                + amount
            )

            if any(word in description for word in risky_words):
                suspicious.append(transaction)

        score = 10

        if total > 0:
            suspicious_total = sum(
                Decimal(str(t["amount"]))
                for t in suspicious
            )

            risk_ratio = suspicious_total / total

            # Штраф за частку ризикових витрат.
            if risk_ratio >= Decimal("0.30"):
                score -= 5
            elif risk_ratio >= Decimal("0.15"):
                score -= 3
            elif suspicious_total > 0:
                score -= 1

        score = max(1, min(10, score))

        return {
            "total": float(total),
            "categories": {
                category: float(amount)
                for category, amount in categories.items()
            },
            "suspicious": suspicious,
            "score": score,
        }

