import logging
from pathlib import Path

from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery, FSInputFile

from config import config
from database import get_user_language, record_download
from handlers.start import check_subscription
from keyboards import build_subscribe_keyboard
from languages import get_strings

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("dl:"))
async def callback_download(call: CallbackQuery, bot: Bot) -> None:
    if call.from_user is None:
        await call.answer()
        return

    user = call.from_user
    language = await get_user_language(user.id)
    s = get_strings(language)
    filename = call.data.removeprefix("dl:")

    # Re-verify subscription before every download
    if not await check_subscription(bot, user.id):
        await call.answer(s["not_subscribed_alert"], show_alert=True)
        try:
            await call.message.edit_text(
                s["not_subscribed_edit"],
                reply_markup=build_subscribe_keyboard(language),
            )
        except TelegramAPIError as exc:
            logger.error(
                "Failed to edit message for user_id=%s: %s", user.id, exc
            )
        return

    file_path = Path(config.FILES_DIR) / filename

    if not file_path.is_file():
        logger.warning("Requested file not found on disk: %s", file_path)
        await call.answer(s["file_not_found_alert"], show_alert=True)
        return

    await call.answer(s["sending_file"].format(filename=filename))

    try:
        await call.message.answer_document(
            document=FSInputFile(path=file_path, filename=filename),
            caption=s["file_caption"].format(filename=filename),
        )
        await record_download(user_id=user.id, filename=filename)
        logger.info("Sent '%s' to user_id=%s.", filename, user.id)

    except FileNotFoundError:
        logger.error("File disappeared before sending: %s", file_path)
        await call.message.answer(s["file_not_found_message"])

    except TelegramAPIError as exc:
        logger.error(
            "Telegram error sending '%s' to user_id=%s: %s",
            filename, user.id, exc,
        )
        await call.message.answer(s["file_send_error"])