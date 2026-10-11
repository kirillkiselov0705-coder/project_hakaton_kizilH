"""Обробники команд Telegram-бота."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from finbot.bot import messages

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(messages.START)


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer(messages.HELP)