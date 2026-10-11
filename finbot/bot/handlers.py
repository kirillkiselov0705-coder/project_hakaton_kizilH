"""Обробники команд Telegram-бота."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from finbot.analysis.score import ScoreCalculator
from finbot.analysis.waste_detector import WasteDetector
from finbot.banking.base import BankingProvider
from finbot.bot import messages
from finbot.bot.formatters import format_statement, format_waste_report


def build_router(
    banking: BankingProvider,
    detector: WasteDetector,
    calculator: ScoreCalculator,
    demo_mode: bool,
) -> Router:
    router = Router()

    def _with_demo_notice(text: str) -> str:
        return f"{messages.DEMO_NOTICE}\n\n{text}" if demo_mode else text

    @router.message(CommandStart())
    async def handle_start(message: Message) -> None:
        await message.answer(messages.START)

    @router.message(Command("help"))
    async def handle_help(message: Message) -> None:
        await message.answer(messages.HELP)

    @router.message(Command("statement"))
    async def handle_statement(message: Message) -> None:
        transactions = await banking.get_transactions(days=30)
        matches = detector.find(transactions)
        score = calculator.calculate(transactions, matches)
        text = f"{format_statement(transactions)}\n\n{format_waste_report(matches, score)}"
        await message.answer(_with_demo_notice(text))

    @router.message(Command("waste"))
    async def handle_waste(message: Message) -> None:
        transactions = await banking.get_transactions(days=30)
        matches = detector.find(transactions)
        score = calculator.calculate(transactions, matches)
        await message.answer(_with_demo_notice(format_waste_report(matches, score)))

    return router