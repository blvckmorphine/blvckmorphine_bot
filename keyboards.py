from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config
from database import get_available_files
from languages import AVAILABLE_LANGUAGES, get_strings


def build_subscribe_keyboard(language: str) -> InlineKeyboardMarkup:
    """Keyboard shown to users who are not subscribed to the channel."""
    s = get_strings(language)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=s["btn_join_channel"], url=config.CHANNEL_LINK),
        ],
        [
            InlineKeyboardButton(
                text=s["btn_check_subscription"],
                callback_data="check_sub",
            ),
        ],
        [
            InlineKeyboardButton(text=s["btn_language"], callback_data="open_language"),
        ],
        [
            InlineKeyboardButton(text=s["btn_support"], url=config.SUPPORT_LINK),
        ],
    ])


def build_files_keyboard(language: str) -> InlineKeyboardMarkup:
    files = get_available_files()
    rows: list[list[InlineKeyboardButton]] = []

    for f in files:
        rows.append([
            InlineKeyboardButton(
                text=f"📁 {f.name}",
                callback_data=f"dl:{f.name}",
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text="🏠 Main Menu",
            callback_data="back_to_start",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_language_keyboard() -> InlineKeyboardMarkup:
    """One button per available language plus a Back button."""
    rows: list[list[InlineKeyboardButton]] = []

    for code, label in AVAILABLE_LANGUAGES.items():
        rows.append([
            InlineKeyboardButton(
                text=label,
                callback_data=f"setlang:{code}",
            )
        ])

    rows.append([
        InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_start"),
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_support_keyboard(language: str) -> InlineKeyboardMarkup:
    """Support screen keyboard with a direct link and a Back button."""
    s = get_strings(language)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=s["btn_support"], url=config.SUPPORT_LINK),
        ],
        [
            InlineKeyboardButton(text=s["btn_back"], callback_data="back_to_start"),
        ],
    ])


def build_no_files_keyboard(language: str) -> InlineKeyboardMarkup:
    """Keyboard shown when the files directory is empty."""
    s = get_strings(language)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=s["btn_language"], callback_data="open_language"),
        ],
        [
            InlineKeyboardButton(text=s["btn_support"], url=config.SUPPORT_LINK),
        ],
    ])


def build_main_menu(language: str) -> InlineKeyboardMarkup:
    s = get_strings(language)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📂 Free FLPs",
                    callback_data="open_files",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📊 Statistics",
                    callback_data="statistics",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=s["btn_language"],
                    callback_data="open_language",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=s["btn_support"],
                    url=config.SUPPORT_LINK,
                ),
            ],
        ]
    )


def build_statistics_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_to_start",
                )
            ]
        ]
    )