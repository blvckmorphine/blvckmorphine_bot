from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    ADMIN_ID: int = 6557216014
    CHANNEL_ID: str = "@blvckmorphine"
    CHANNEL_LINK: str = "https://t.me/blvckmorphine"
    SUPPORT_LINK: str = "https://t.me/blvkkkkkk"
    FILES_DIR: str = "files"
    DB_PATH: str = "users.db"
    ALLOWED_EXTENSIONS: tuple[str, ...] = (".zip", ".flp")
    DEFAULT_LANGUAGE: str = "en"


config = Config()