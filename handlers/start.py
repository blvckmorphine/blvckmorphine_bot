import logging

from aiogram import Bot, Router
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import config
from database import get_available_files, upsert_user, get_user_language
from keyboards import (
    build_main_menu,
    build_files_keyboard,
    build_no_files_keyboard,
    build_subscribe_keyboard,
)
from languages import get_strings

logger = logging.getLogger(__name__)

router = Router()

SUBSCRIBED_STATUSES = {
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.CREATOR,
}


async def check_subscription(bot: Bot, user_id: int) -> bool:
    """Return True if the user is a member, admin, or creator of the channel."""
    try:
        member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        return member.status in SUBSCRIBED_STATUSES
    except TelegramAPIError as exc:
        logger.error("get_chat_member error for user_id=%s: %s", user_id, exc)
        return False


async def send_main_menu(
    target: Message | CallbackQuery,
    bot: Bot,
    user_id: int,
    full_name: str,
    language: str,
    edit: bool = False,
) -> None:
    """
    Send or edit the main menu depending on subscription status.
    If edit=True, the existing message will be edited instead of sending a new one.
    """
    s = get_strings(language)
    subscribed = await check_subscription(bot, user_id)

    if subscribed:
        files = get_available_files()
        if files:
            text = s["welcome_subscribed"].format(full_name=full_name)
            keyboard = build_main_menu(language)
        else:
            text = s["no_files_available"]
            keyboard = build_no_files_keyboard(language)
    else:
        text = s["welcome_not_subscribed"].format(full_name=full_name)
        keyboard = build_subscribe_keyboard(language)

    message = target if isinstance(target, Message) else target.message

    if edit:
        try:
            await message.edit_text(text, reply_markup=keyboard)
        except TelegramAPIError:
            await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot) -> None:
    print("START HANDLER")

    if message.from_user is None:
        return

    user = message.from_user


    await upsert_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
    )

    language = await get_user_language(user.id)

    await send_main_menu(
        target=message,
        bot=bot,
        user_id=user.id,
        full_name=user.full_name,
        language=language,
        edit=False,
    )


@router.callback_query(lambda c: c.data == "check_sub")
async def callback_check_sub(call: CallbackQuery, bot: Bot) -> None:
    if call.from_user is None:
        await call.answer()
        return

    user = call.from_user
    language = await get_user_language(user.id)
    s = get_strings(language)
    subscribed = await check_subscription(bot, user.id)

    if subscribed:
        await call.answer(s["subscription_confirmed"])
        await send_main_menu(
            target=call,
            bot=bot,
            user_id=user.id,
            full_name=user.full_name,
            language=language,
            edit=True,
        )
    else:
        await call.answer(s["not_subscribed_alert"], show_alert=True)


@router.callback_query(lambda c: c.data == "back_to_start")
async def callback_back_to_start(call: CallbackQuery, bot: Bot) -> None:
    if call.from_user is None:
        await call.answer()
        return

    user = call.from_user
    language = await get_user_language(user.id)

    await call.answer()
    await send_main_menu(
        target=call,
        bot=bot,
        user_id=user.id,
        full_name=user.full_name,
        language=language,
        edit=True,
    )


@router.callback_query(lambda c: c.data == "open_files")
async def open_files(call: CallbackQuery):
    if call.from_user is None:
        await call.answer()
        return

    language = await get_user_language(call.from_user.id)

    await call.message.edit_text(
        "📂 Available FLPs:",
        reply_markup=build_files_keyboard(language),
    )

    await call.answer()