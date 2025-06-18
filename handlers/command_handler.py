from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from facade import user_facade
from models.user import User
from service import user_service

router = Router()


@router.message(CommandStart())
async def handle_start_command(message: Message):
    tg_id = message.from_user.id
    tg_username = message.from_user.username

    user = await User.get_or_none(tg_id=tg_id)

    if user:
        if user.tg_username != tg_username:
            user.tg_username = tg_username
            await user.save()
        await message.answer("✅ Ты уже зарегистрирован!")
        return

    # Проверка: есть ли username
    if not tg_username:
        await message.answer("❗️ У тебя нет @username. Установи его в Telegram, чтобы пользоваться ботом.")
        return

    # Создаём нового пользователя
    user = await user_facade.create_user(tg_username, tg_id)
    await message.answer(f"🎉 Добро пожаловать, @{user.tg_username}! Ты успешно зарегистрирован.")
