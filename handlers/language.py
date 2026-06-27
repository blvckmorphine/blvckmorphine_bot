import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery

from database import get_user_language, set_user_language
from handlers.start import send_main_menu
from keyboards import build_language_keyboard
from languages import AVAILABLE_LANGUAGES, get_strings

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "open_language")
async def callback_open_language(call: CallbackQuery) -> None:
    """Show the language selection menu."""
    if call.from_user is None:
        await call.answer()
        return

    language = await get_user_language(call.from_user.id)
    s = get_strings(language)

    await call.answer()
    try:
        await call.message.edit_text(
            s["choose_language"],
            reply_markup=build_language_keyboard(),
        )
    except TelegramAPIError as exc:
        logger.error(
            "Failed to edit language menu for user_id=%s: %s",
            call.from_user.id, exc,
        )


@router.callback_query(lambda c: c.data and c.data.startswith("setlang:"))
async def callback_set_language(call: CallbackQuery, bot: Bot) -> None:
    """Persist the chosen language and return the user to the main menu."""
    if call.from_user is None:
        await call.answer()
        return

    user = call.from_user
    lang_code = call.data.removeprefix("setlang:")

    if lang_code not in AVAILABLE_LANGUAGES:
        await call.answer("⚠️ Unknown language.", show_alert=True)
        return

    await set_user_language(user_id=user.id, language=lang_code)
    logger.info("user_id=%s set language to '%s'.", user.id, lang_code)

    s = get_strings(lang_code)
    await call.answer(s["language_set"], show_alert=False)

    await send_main_menu(
        target=call,
        bot=bot,
        user_id=user.id,
        full_name=user.full_name,
        language=lang_code,
        edit=True,
    )