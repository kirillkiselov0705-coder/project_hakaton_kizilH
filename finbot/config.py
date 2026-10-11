"""Завантаження налаштувань застосунку зі змінних середовища."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Незмінний набір налаштувань. Секрети приховані з repr, щоб не потрапити в логи."""

    telegram_bot_token: str = field(repr=False)
    monobank_token: str = field(repr=False)
    llm_api_key: str = field(repr=False)
    llm_model: str
    demo_mode: bool
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            monobank_token=os.getenv("MONOBANK_TOKEN", ""),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", ""),
            demo_mode=_to_bool(os.getenv("DEMO_MODE", "true")),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )