from telethon.sync import TelegramClient
import os

from config import bot_config

# Название сессии — сохраняется как telethon.session файл
SESSION_NAME = "bot_session"

# Создаём клиент (вход в контекст НЕ здесь)
client = TelegramClient(SESSION_NAME, bot_config.TG_API_ID, bot_config.TG_API_HASH)
