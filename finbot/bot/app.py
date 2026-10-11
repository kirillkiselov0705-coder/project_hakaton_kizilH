"""Створення та запуск Telegram-бота."""

import logging

from aiogram import Bot, Dispatcher

from finbot.bot.handlers import router
from finbot.config import Settings

logger = logging.getLogger(__name__)


async def run_bot(settings: Settings) -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError(
            "Не задано TELEGRAM_BOT_TOKEN. Додайте токен у файл .env."
        )

    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    logger.info("Бот запускається")
    await dispatcher.start_polling(bot)