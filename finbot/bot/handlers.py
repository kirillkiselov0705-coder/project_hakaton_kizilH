"""Обробники команд Telegram-бота."""

import httpx
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from finbot.analysis.score import ScoreCalculator
from finbot.analysis.waste_detector import WasteDetector
from finbot.banking.monobank import InvalidTokenError, MonobankError, RateLimitError
from finbot.banking.resolver import BankingResolver
from finbot.bot import messages
from finbot.bot.formatters import format_statement, format_waste_report

CONNECT_CALLBACK = "connect"


class ConnectStates(StatesGroup):
    waiting_token = State()


def _connect_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=messages.CONNECT_BUTTON, callback_data=CONNECT_CALLBACK
                )
            ]
        ]
    )


def build_router(
    resolver: BankingResolver,
    detector: WasteDetector,
    calculator: ScoreCalculator,
) -> Router:
    router = Router()

    async def _load(message: Message):
        """Повертає (транзакції, чи демо) або None, якщо відповідь уже надіслано."""
        user_id = message.chat.id
        provider = resolver.for_user(user_id)
        if provider is None:
            await message.answer(
                messages.NOT_CONNECTED, reply_markup=_connect_keyboard()
            )
            return None
        try:
            transactions = await provider.get_transactions(days=30)
        except RateLimitError:
            await message.answer(messages.RATE_LIMIT)
            return None
        except (MonobankError, httpx.HTTPError):
            await message.answer(messages.BANK_ERROR)
            return None
        return transactions, not resolver.is_connected(user_id)

    @router.message(CommandStart())
    async def handle_start(message: Message) -> None:
        if resolver.is_connected(message.from_user.id):
            await message.answer(messages.START_CONNECTED)
        else:
            await message.answer(messages.START, reply_markup=_connect_keyboard())

    @router.message(Command("help"))
    async def handle_help(message: Message) -> None:
        await message.answer(messages.HELP)

    @router.message(Command("connect"))
    async def handle_connect(message: Message, state: FSMContext) -> None:
        await state.set_state(ConnectStates.waiting_token)
        await message.answer(messages.CONNECT_INSTRUCTIONS)

    @router.callback_query(F.data == CONNECT_CALLBACK)
    async def handle_connect_button(callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(ConnectStates.waiting_token)
        await callback.message.answer(messages.CONNECT_INSTRUCTIONS)
        await callback.answer()

    @router.message(Command("cancel"))
    async def handle_cancel(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(messages.CANCELLED)

    @router.message(Command("disconnect"))
    async def handle_disconnect(message: Message) -> None:
        resolver.disconnect(message.from_user.id)
        await message.answer(messages.DISCONNECTED)

    @router.message(Command("statement"))
    async def handle_statement(message: Message) -> None:
        loaded = await _load(message)
        if loaded is None:
            return
        transactions, is_demo = loaded
        matches = detector.find(transactions)
        score = calculator.calculate(transactions, matches)
        text = f"{format_statement(transactions)}\n\n{format_waste_report(matches, score)}"
        if is_demo:
            text = f"{messages.DEMO_NOTICE}\n\n{text}"
        await message.answer(text)

    @router.message(Command("waste"))
    async def handle_waste(message: Message) -> None:
        loaded = await _load(message)
        if loaded is None:
            return
        transactions, is_demo = loaded
        matches = detector.find(transactions)
        score = calculator.calculate(transactions, matches)
        text = format_waste_report(matches, score)
        if is_demo:
            text = f"{messages.DEMO_NOTICE}\n\n{text}"
        await message.answer(text)

    # Має бути останнім: ловить токен, коли очікується підключення.
    @router.message(ConnectStates.waiting_token, F.text, ~F.text.startswith("/"))
    async def handle_token(message: Message, state: FSMContext) -> None:
        token = message.text.strip()
        try:
            await message.delete()  # прибираємо токен із чату
        except TelegramBadRequest:
            pass
        try:
            await resolver.connect(message.from_user.id, token)
        except InvalidTokenError:
            await message.answer(messages.INVALID_TOKEN)
            return
        except RateLimitError:
            await message.answer(messages.RATE_LIMIT)
            return
        except (MonobankError, httpx.HTTPError):
            await message.answer(messages.BANK_ERROR)
            return
        await state.clear()
        await message.answer(messages.CONNECTED)

    return router