from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import (
    get_total_users,
    get_total_downloads,
    get_top_downloads,
    get_available_files,
    get_user_language,
)

from keyboards import build_statistics_keyboard

router = Router()


@router.callback_query(F.data == "statistics")
async def statistics(callback: CallbackQuery):

    if callback.from_user is None:
        await callback.answer()
        return

    await get_user_language(callback.from_user.id)

    users = await get_total_users()
    downloads = await get_total_downloads()
    files = len(get_available_files())
    top = await get_top_downloads()

    text = (
        "📊 Statistics\n\n"
        f"👥 Total Users: {users}\n"
        f"📥 Total Downloads: {downloads}\n"
        f"📂 Available FLPs: {files}\n\n"
        "🔥 Most Downloaded:\n"
    )

    if top:
        for i, (filename, count) in enumerate(top, start=1):
            text += f"{i}. {filename} ({count})\n"
    else:
        text += "No downloads yet."

    await callback.answer()

    try:
        await callback.message.edit_text(
            text,
            reply_markup=build_statistics_keyboard(),
        )
    except Exception as e:
        print("STATISTICS ERROR:", repr(e))