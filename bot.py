import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import config
from database import init_db
from handlers import admin, files, language, start, support, statistics

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Bot & Dispatcher
# ---------------------------------------------------------------------------

from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------

dp.include_router(start.router)
dp.include_router(files.router)
dp.include_router(language.router)
dp.include_router(support.router)
dp.include_router(statistics.router)
dp.include_router(admin.router)

# ---------------------------------------------------------------------------
# Startup & Shutdown
# ---------------------------------------------------------------------------

async def on_startup() -> None:
    """Run once when the bot starts: create directories and initialize DB."""
    Path(config.FILES_DIR).mkdir(parents=True, exist_ok=True)
    await init_db()
    me = await bot.get_me()
    logger.info("Bot @%s is online and polling.", me.username)


async def on_shutdown() -> None:
    """Run once when the bot shuts down: close the bot session cleanly."""
    logger.info("Bot is shutting down. Closing session.")
    await bot.session.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Starting polling…")
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    asyncio.run(main())