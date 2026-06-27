import logging

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from database import get_user_language
from keyboards import build_support_keyboard
from languages import get_strings

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("support"))
async def cmd_support(message: Message) -> None:
    """Send the support message when the user types /support."""
    if message.from_user is None:
        return

    language = await get_user_language(message.from_user.id)
    s = get_strings(language)

    await message.answer(
        s["support_message"],
        reply_markup=build_support_keyboard(language),
    )


@router.callback_query(lambda c: c.data == "open_support")
async def callback_open_support(call: CallbackQuery) -> None:
    """Show the support screen when the user taps the Support button."""
    if call.from_user is None:
        await call.answer()
        return

    user = call.from_user
    language = await get_user_language(user.id)
    s = get_strings(language)

    await call.answer()
    try:
        await call.message.edit_text(
            s["support_message"],
            reply_markup=build_support_keyboard(language),
        )
    except TelegramAPIError as exc:
        logger.error(
            "Failed to edit support message for user_id=%s: %s",
            user.id, exc,
        )
        try:
            await call.message.answer(
                s["support_message"],
                reply_markup=build_support_keyboard(language),
            )
        except TelegramAPIError as exc2:
            logger.error(
                "Failed to send support message for user_id=%s: %s",
                user.id, exc2,
            )