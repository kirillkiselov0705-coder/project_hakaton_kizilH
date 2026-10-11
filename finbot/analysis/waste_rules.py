"""Правила визначення «порожніх» витрат: категорії, ключові слова, вага."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WasteCategory:
    key: str
    title: str
    keywords: tuple[str, ...]
    weight: float = 1.0


WASTE_CATEGORIES: tuple[WasteCategory, ...] = (
    WasteCategory(
        key="gambling",
        title="Азартні ігри та ставки",
        keywords=(
            "casino", "казино", "pin-up", "pinup", "1xbet", "parimatch",
            "betway", "vulkan", "вулкан", "букмекер", "ставки", "slots",
            "слоти", "jackpot", "джекпот", "poker", "покер",
        ),
        weight=1.5,
    ),
    WasteCategory(
        key="adult",
        title="Контент для дорослих",
        keywords=("porn", "xxx", "onlyfans", "18+", "adult", "sex"),
        weight=1.2,
    ),
    WasteCategory(
        key="lottery",
        title="Лотереї",
        keywords=("лотере", "lottery"),
        weight=0.8,
    ),
    WasteCategory(
        key="esoterics",
        title="Ворожіння та езотерика",
        keywords=("таролог", "tarot", "астролог", "ворожб", "гороскоп"),
        weight=0.6,
    ),
)