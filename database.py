import logging
from datetime import datetime
from pathlib import Path

import aiosqlite

from config import config

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Initialize the database and create all tables if they don't exist."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                full_name   TEXT NOT NULL,
                language    TEXT NOT NULL DEFAULT 'en',
                joined_at   TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS downloads (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                filename        TEXT NOT NULL,
                downloaded_at   TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await db.commit()
    logger.info("Database initialized at '%s'.", config.DB_PATH)


async def upsert_user(
    user_id: int,
    username: str | None,
    full_name: str,
    language: str | None = None,
) -> None:
    """Insert a new user or update username/full_name. Optionally update language."""
    now = datetime.utcnow().isoformat()
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            if language is not None:
                await db.execute("""
                    INSERT INTO users (user_id, username, full_name, language, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username  = excluded.username,
                        full_name = excluded.full_name,
                        language  = excluded.language
                """, (user_id, username, full_name, language, now))
            else:
                await db.execute("""
                    INSERT INTO users (user_id, username, full_name, language, joined_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username  = excluded.username,
                        full_name = excluded.full_name
                """, (user_id, username, full_name, config.DEFAULT_LANGUAGE, now))
            await db.commit()
    except aiosqlite.Error as exc:
        logger.error("upsert_user failed for user_id=%s: %s", user_id, exc)


async def get_user_language(user_id: int) -> str:
    """Return the stored language code for a user, defaulting to config default."""
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            async with db.execute(
                "SELECT language FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row[0]
                return config.DEFAULT_LANGUAGE
    except aiosqlite.Error as exc:
        logger.error("get_user_language failed for user_id=%s: %s", user_id, exc)
        return config.DEFAULT_LANGUAGE


async def set_user_language(user_id: int, language: str) -> None:
    """Update the language preference for an existing user."""
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            await db.execute(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id),
            )
            await db.commit()
    except aiosqlite.Error as exc:
        logger.error("set_user_language failed for user_id=%s: %s", user_id, exc)


async def record_download(user_id: int, filename: str) -> None:
    """Log a file download event."""
    now = datetime.utcnow().isoformat()
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            await db.execute(
                "INSERT INTO downloads (user_id, filename, downloaded_at) VALUES (?, ?, ?)",
                (user_id, filename, now),
            )
            await db.commit()
    except aiosqlite.Error as exc:
        logger.error(
            "record_download failed for user_id=%s file=%s: %s", user_id, filename, exc
        )


async def get_total_users() -> int:
    """Return the total number of unique registered users."""
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    except aiosqlite.Error as exc:
        logger.error("get_total_users failed: %s", exc)
        return 0


async def get_total_downloads() -> int:
    """Return the total number of download events across all users."""
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            async with db.execute("SELECT COUNT(*) FROM downloads") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    except aiosqlite.Error as exc:
        logger.error("get_total_downloads failed: %s", exc)
        return 0


async def get_top_downloads(limit: int = 5) -> list[tuple[str, int]]:
    """Return the most downloaded files as a list of (filename, count) tuples."""
    try:
        async with aiosqlite.connect(config.DB_PATH) as db:
            async with db.execute("""
                SELECT filename, COUNT(*) AS cnt
                FROM downloads
                GROUP BY filename
                ORDER BY cnt DESC
                LIMIT ?
            """, (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [(row[0], row[1]) for row in rows]
    except aiosqlite.Error as exc:
        logger.error("get_top_downloads failed: %s", exc)
        return []


def get_available_files() -> list[Path]:
    """Return a sorted list of allowed files from the files directory."""
    files_dir = Path(config.FILES_DIR)
    if not files_dir.is_dir():
        logger.warning("Files directory '%s' does not exist.", files_dir)
        return []
    return sorted(
        f for f in files_dir.iterdir()
        if f.is_file() and f.suffix.lower() in config.ALLOWED_EXTENSIONS
    )