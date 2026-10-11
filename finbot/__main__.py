"""Точка входу застосунку."""

import logging

from finbot.config import Settings
from finbot.logging_setup import setup_logging


def main() -> None:
    settings = Settings.from_env()
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Конфігурацію завантажено: %s", settings)


if __name__ == "__main__":
    main()