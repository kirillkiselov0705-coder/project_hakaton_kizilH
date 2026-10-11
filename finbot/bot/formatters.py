"""Форматування даних для повідомлень бота."""

from finbot.analysis.score import FinanceScore
from finbot.analysis.waste_detector import WasteMatch
from finbot.bot import messages
from finbot.domain.models import Transaction


def format_statement(transactions: list[Transaction], limit: int = 10) -> str:
    if not transactions:
        return "За обраний період транзакцій не знайдено."

    lines = ["Останні транзакції:"]
    for t in transactions[:limit]:
        sign = "+" if t.amount_kopecks > 0 else "-"
        lines.append(
            f"{t.time:%d.%m.%Y} | {t.description} | {sign}{abs(t.amount):.2f} грн"
        )
    return "\n".join(lines)


def format_score(score: FinanceScore) -> str:
    return "\n".join(
        [
            messages.SCORE_LINE.format(
                value=score.value, level=messages.SCORE_LEVELS[score.level]
            ),
            messages.WASTE_SHARE_LINE.format(share=score.waste_share * 100),
        ]
    )


def format_waste_report(matches: list[WasteMatch], score: FinanceScore) -> str:
    if not matches:
        return f"{messages.WASTE_NONE}\n\n{format_score(score)}"

    by_category: dict[str, list[WasteMatch]] = {}
    for match in matches:
        by_category.setdefault(match.category.key, []).append(match)

    lines = [messages.WASTE_HEADER]
    for key, items in by_category.items():
        total = sum(abs(item.transaction.amount) for item in items)
        lines.append("")
        lines.append(f"{items[0].category.title}: {len(items)} шт., разом {total:.2f} грн.")
        lines.append(messages.LECTURES[key])
    lines.append("")
    lines.append(format_score(score))
    return "\n".join(lines)