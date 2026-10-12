
from decimal import Decimal

from finbot.llm.analyzer import TransactionAnalyzer
from finbot.llm.risk_classifier import RiskClassifier


class FinancialService:

    def __init__(self):
        self.analyzer = TransactionAnalyzer()
        self.classifier = RiskClassifier()

    async def analyze(self, transactions: list[dict]) -> dict:

        classified_transactions = []
        confirmed_risks = []
        suspected_risks = []

        for transaction in transactions:
            result = await self.classifier.classify(transaction)

            classified = {
                **transaction,
                "risk_category": result["category"],
                "risk_level": result["risk_level"],
                "risk_status": result["status"],
                "risk_reason": result["reason"],
                "recommendation": result["recommendation"],
            }

            classified_transactions.append(classified)

            if result["category"] not in ("gambling", "adult"):
                continue

            if result["status"] == "confirmed":
                confirmed_risks.append(classified)

            elif result["status"] == "suspected":
                suspected_risks.append(classified)

        analysis = self.analyzer.analyze(transactions)

        total = Decimal(str(analysis["total"]))

        confirmed_total = sum(
            (
                Decimal(str(t["amount"]))
                for t in confirmed_risks
                if Decimal(str(t["amount"])) > 0
            ),
            Decimal("0"),
        )

        score = 10

        if total > 0:
            ratio = confirmed_total / total

            if ratio >= Decimal("0.30"):
                score -= 5
            elif ratio >= Decimal("0.15"):
                score -= 3
            elif confirmed_total > 0:
                score -= 1

        analysis["score"] = max(1, min(10, score))

        # Для сумісності зі старим інтерфейсом
        analysis["suspicious"] = confirmed_risks

        analysis["confirmed_risks"] = confirmed_risks
        analysis["suspected_risks"] = suspected_risks
        analysis["transactions"] = classified_transactions

        return analysis
