from typing import TypedDict


class LangStrings(TypedDict):
    welcome_subscribed: str
    welcome_not_subscribed: str
    no_files_available: str
    subscription_confirmed: str
    not_subscribed_alert: str
    not_subscribed_edit: str
    sending_file: str
    file_not_found_alert: str
    file_not_found_message: str
    file_send_error: str
    file_caption: str
    choose_language: str
    language_set: str
    support_message: str
    stats_header: str
    stats_users: str
    stats_downloads: str
    stats_file_count: str
    stats_top_header: str
    stats_no_downloads: str
    stats_top_entry: str
    admin_only: str
    btn_join_channel: str
    btn_check_subscription: str
    btn_support: str
    btn_language: str
    btn_files: str
    btn_back: str


LANGUAGES: dict[str, LangStrings] = {
    "en": LangStrings(
        welcome_subscribed=(
            "👋 Welcome, <b>{full_name}</b>!\n\n"
            "Here are all available files. Tap one to download:"
        ),
        welcome_not_subscribed=(
            "👋 Welcome, <b>{full_name}</b>!\n\n"
            "To access the files you must first subscribe to our channel."
        ),
        no_files_available=(
            "👋 Welcome!\n\nNo files are available yet. Check back soon."
        ),
        subscription_confirmed="✅ Subscription confirmed!",
        not_subscribed_alert="❌ You are not subscribed yet. Please join the channel first.",
        not_subscribed_edit="You need to join our channel to download files:",
        sending_file="⏳ Sending {filename}…",
        file_not_found_alert="⚠️ File not found. Please try again later.",
        file_not_found_message="⚠️ The file could not be found on the server.",
        file_send_error="⚠️ Failed to send the file. Please try again later.",
        file_caption="📁 <b>{filename}</b>",
        choose_language="🌐 Please choose your language:",
        language_set="✅ Language set to <b>English</b>.",
        support_message=(
            "💬 <b>Support</b>\n\n"
            "Need help? Reach out to us directly via the button below."
        ),
        stats_header="📊 <b>Bot Statistics</b>\n\n",
        stats_users="👤 Total users: <b>{count}</b>\n",
        stats_downloads="📥 Total downloads: <b>{count}</b>\n",
        stats_file_count="📁 Files in /files: <b>{count}</b>\n\n",
        stats_top_header="🏆 <b>Top Downloaded Files:</b>\n",
        stats_no_downloads="  No downloads recorded yet.",
        stats_top_entry="  {rank}. <code>{filename}</code> — {count} download{plural}\n",
        admin_only="⛔ You are not authorised to use this command.",
        btn_join_channel="📢 Join Channel",
        btn_check_subscription="✅ Check Subscription",
        btn_support="💬 Support",
        btn_language="🌐 Language",
        btn_files="📁 Files",
        btn_back="⬅️ Back",
    ),
    "ru": LangStrings(
        welcome_subscribed=(
            "👋 Добро пожаловать, <b>{full_name}</b>!\n\n"
            "Вот все доступные файлы. Нажмите на файл для скачивания:"
        ),
        welcome_not_subscribed=(
            "👋 Добро пожаловать, <b>{full_name}</b>!\n\n"
            "Для доступа к файлам сначала подпишитесь на наш канал."
        ),
        no_files_available=(
            "👋 Добро пожаловать!\n\nФайлы пока недоступны. Загляните позже."
        ),
        subscription_confirmed="✅ Подписка подтверждена!",
        not_subscribed_alert="❌ Вы ещё не подписаны. Сначала вступите в канал.",
        not_subscribed_edit="Чтобы скачать файлы, вступите в наш канал:",
        sending_file="⏳ Отправляю {filename}…",
        file_not_found_alert="⚠️ Файл не найден. Попробуйте позже.",
        file_not_found_message="⚠️ Файл не найден на сервере.",
        file_send_error="⚠️ Не удалось отправить файл. Попробуйте позже.",
        file_caption="📁 <b>{filename}</b>",
        choose_language="🌐 Выберите язык:",
        language_set="✅ Язык установлен: <b>Русский</b>.",
        support_message=(
            "💬 <b>Поддержка</b>\n\n"
            "Нужна помощь? Свяжитесь с нами через кнопку ниже."
        ),
        stats_header="📊 <b>Статистика бота</b>\n\n",
        stats_users="👤 Всего пользователей: <b>{count}</b>\n",
        stats_downloads="📥 Всего скачиваний: <b>{count}</b>\n",
        stats_file_count="📁 Файлов в /files: <b>{count}</b>\n\n",
        stats_top_header="🏆 <b>Топ скачиваний:</b>\n",
        stats_no_downloads="  Скачиваний пока нет.",
        stats_top_entry="  {rank}. <code>{filename}</code> — {count} скачивани{plural}\n",
        admin_only="⛔ У вас нет прав для использования этой команды.",
        btn_join_channel="📢 Вступить в канал",
        btn_check_subscription="✅ Проверить подписку",
        btn_support="💬 Поддержка",
        btn_language="🌐 Язык",
        btn_files="📁 Файлы",
        btn_back="⬅️ Назад",
    ),
}

AVAILABLE_LANGUAGES: dict[str, str] = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
}


def get_strings(language: str) -> LangStrings:
    """Return the LangStrings for the given language code, falling back to English."""
    return LANGUAGES.get(language, LANGUAGES["en"])


def pluralize_downloads(count: int, language: str) -> str:
    """Return the correct plural suffix for 'downloads' in the given language."""
    if language == "en":
        return "s" if count != 1 else ""
    if language == "ru":
        last_two = count % 100
        last_one = count % 10
        if 11 <= last_two <= 14:
            return "й"
        if last_one == 1:
            return "е"
        if 2 <= last_one <= 4:
            return "я"
        return "й"
    return "s" if count != 1 else ""