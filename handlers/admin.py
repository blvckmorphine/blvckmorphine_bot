import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import config
from database import (
    get_available_files,
    get_top_downloads,
    get_total_downloads,
    get_total_users,
)
from languages import get_strings, pluralize_downloads

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    """Display bot statistics. Restricted to ADMIN_ID only."""
    if message.from_user is None:
        return

    if message.from_user.id != config.ADMIN_ID:
        # Always respond in English for unauthorized access attempts
        s = get_strings("en")
        await message.answer(s["admin_only"])
        logger.warning(
            "Unauthorized /stats attempt by user_id=%s username=%s.",
            message.from_user.id,
            message.from_user.username,
        )
        return

    # Admin always sees stats in English
    s = get_strings("en")

    total_users = await get_total_users()
    total_downloads = await get_total_downloads()
    top = await get_top_downloads(limit=5)
    file_count = len(get_available_files())

    top_lines = ""
    for i, (fname, cnt) in enumerate(top):
        plural = pluralize_downloads(cnt, "en")
        top_lines += s["stats_top_entry"].format(
            rank=i + 1,
            filename=fname,
            count=cnt,
            plural=plural,
        )

    if not top_lines:
        top_lines = s["stats_no_downloads"]

    text = (
        s["stats_header"]
        + s["stats_users"].format(count=total_users)
        + s["stats_downloads"].format(count=total_downloads)
        + s["stats_file_count"].format(count=file_count)
        + s["stats_top_header"]
        + top_lines
    )

    await message.answer(text)
    logger.info("Admin user_id=%s requested /stats.", message.from_user.id)


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message) -> None:
    """
    Placeholder for future broadcast functionality.
    Currently informs the admin that it is not yet implemented.
    Restricted to ADMIN_ID only.
    """
    if message.from_user is None:
        return

    if message.from_user.id != config.ADMIN_ID:
        s = get_strings("en")
        await message.answer(s["admin_only"])
        logger.warning(
            "Unauthorized /broadcast attempt by user_id=%s username=%s.",
            message.from_user.id,
            message.from_user.username,
        )
        return

    await message.answer(
        "📣 <b>Broadcast</b>\n\n"
        "To use broadcast, reply to this message with the text you want to send "
        "to all users.\n\n"
        "<i>This feature is reserved for future implementation.</i>"
    )