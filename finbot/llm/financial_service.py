
from decimal import Decimal

from finbot.llm.analyzer import TransactionAnalyzer
from finbot.llm.risk_classifier import RiskClassifier


class FinancialService:

    def __init__(self):
        self.analyzer = TransactionAnalyzer()
        self.classifier = RiskClassifier()

    async def analyze(self, transactions: list[dict]) -> dict:

        classified_transactions = []

        for transaction in transactions:
            result = await self.classifier.classify(transaction)

            classified_transactions.append({
                **transaction,
                "risk_category": result["category"],
                "risk_level": result["risk_level"],
                "risk_reason": result["reason"],
                "recommendation": result["recommendation"],
            })

        analysis = self.analyzer.analyze(transactions)

        suspicious = [
            transaction
            for transaction in classified_transactions
            if transaction["risk_category"] in ("gambling", "adult")
            and transaction["risk_level"] in ("high", "medium")
        ]

        total = Decimal(str(analysis["total"]))

        suspicious_total = sum(
            (
                Decimal(str(t["amount"]))
                for t in suspicious
                if Decimal(str(t["amount"])) > 0
            ),
            Decimal("0"),
        )

        score = 10

        if total > 0:
            ratio = suspicious_total / total

            if ratio >= Decimal("0.30"):
                score -= 5
            elif ratio >= Decimal("0.15"):
                score -= 3
            elif suspicious_total > 0:
                score -= 1

        analysis["score"] = max(1, min(10, score))
        analysis["suspicious"] = suspicious
        analysis["transactions"] = classified_transactions

        return analysis
