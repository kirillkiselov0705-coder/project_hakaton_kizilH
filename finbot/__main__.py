"""Точка входу застосунку."""

import asyncio
import logging

from finbot.bot.app import run_bot
from finbot.config import Settings
from finbot.logging_setup import setup_logging


def main() -> None:
    settings = Settings.from_env()
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Конфігурацію завантажено: %s", settings)

    try:
        asyncio.run(run_bot(settings))
    except KeyboardInterrupt:
        logger.info("Бота зупинено")


if __name__ == "__main__":
    main()