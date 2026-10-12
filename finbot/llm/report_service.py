
from finbot.llm.financial_service import FinancialService
from finbot.llm.ollama_assistant import OllamaAssistant


class ReportService:

    def __init__(self):
        self.financial_service = FinancialService()
        self.assistant = OllamaAssistant()

    async def generate(
        self,
        question: str,
        transactions: list[dict],
    ) -> str:

        if not await self.assistant.is_finance_topic(question):
            return (
                "Я не розрахован на такі питання, "
                "В МЕНЕ ХИТРЕ ЛИЦЕ"
            )

        analysis = await self.financial_service.analyze(
            transactions
        )

        recommendations = await self.assistant.answer(
            question,
            transactions,
            analysis,
        )

        score = analysis["score"]
        total = analysis["total"]

        lines = [
            "ФІНАНСОВИЙ ЗВІТ",
            "",
            f"Загальні витрати: {total:.2f} грн",
            f"Загальна оцінка витрат: {score}/10",
            "",
            "Підтверджені категорії ризику:",
        ]

        confirmed = analysis["confirmed_risks"]

        if confirmed:
            for transaction in confirmed:
                lines.append(
                    f"- {transaction['description']}: "
                    f"{transaction['amount']} грн"
                )
        else:
            lines.append("Не виявлено.")

        lines.extend([
            "",
            "Операції для додаткової перевірки:",
        ])

        suspected = analysis["suspected_risks"]

        if suspected:
            for transaction in suspected:
                lines.append(
                    f"- {transaction['description']}: "
                    f"{transaction['amount']} грн"
                )
        else:
            lines.append("Не виявлено.")

        lines.extend([
            "",
            "Рекомендації:",
            recommendations,
        ])

        return "\n".join(lines)
