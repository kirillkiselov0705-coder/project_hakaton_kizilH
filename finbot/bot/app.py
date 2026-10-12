"""Створення та запуск Telegram-бота."""

import logging

import httpx
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from finbot.analysis.score import ScoreCalculator
from finbot.analysis.waste_detector import WasteDetector
from finbot.banking.resolver import BankingResolver
from finbot.bot.handlers import build_router
from finbot.config import Settings

logger = logging.getLogger(__name__)

COMMANDS = [
    BotCommand(command="start", description="Початок роботи"),
    BotCommand(command="help", description="Довідка"),
    BotCommand(command="connect", description="Підключити monobank"),
    BotCommand(command="disconnect", description="Відключити monobank"),
    BotCommand(command="statement", description="Виписка за 30 днів"),
    BotCommand(command="waste", description="Перевірка на порожні витрати"),
    BotCommand(command="cancel", description="Скасувати підключення"),
]


async def run_bot(settings: Settings) -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError(
            "Не задано TELEGRAM_BOT_TOKEN. Додайте токен у файл .env."
        )

    async with httpx.AsyncClient(timeout=15) as http:
        resolver = BankingResolver(http, demo_mode=settings.demo_mode)
        bot = Bot(token=settings.telegram_bot_token)
        dispatcher = Dispatcher()
        dispatcher.include_router(
            build_router(resolver, WasteDetector(), ScoreCalculator())
        )

        await bot.set_my_commands(COMMANDS)

        logger.info("Бот запускається")
        await dispatcher.start_polling(bot)