"""Створення та запуск Telegram-бота."""

import logging

from aiogram import Bot, Dispatcher

from finbot.analysis.score import ScoreCalculator
from finbot.analysis.waste_detector import WasteDetector
from finbot.banking.demo import DemoBankingProvider
from finbot.bot.handlers import build_router
from finbot.config import Settings

logger = logging.getLogger(__name__)


async def run_bot(settings: Settings) -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError(
            "Не задано TELEGRAM_BOT_TOKEN. Додайте токен у файл .env."
        )

    # Реальний провайдер monobank підключимо в частині 5.3.
    banking = DemoBankingProvider()
    detector = WasteDetector()
    calculator = ScoreCalculator()

    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(
        build_router(banking, detector, calculator, demo_mode=settings.demo_mode)
    )

    logger.info("Бот запускається")
    await dispatcher.start_polling(bot)