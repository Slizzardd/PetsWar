from typing import Callable, Awaitable, Dict, Any

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

import keyboards.keyboards as kb
from models.user import User


class AutoRegisterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        # Пропускаем проверку для команды /start
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)

        tg_id = event.from_user.id
        current_username = event.from_user.username
        user = await User.get_or_none(tg_id=tg_id)

        if not user:
            await event.answer(
                f'@{event.from_user.username}, для пользования функциями бота, перейди по ссылке:',
                reply_markup=kb.generate_link_to_bot(),
                disable_web_page_preview=True
            )
            return

        if user.tg_username != current_username:
            user.tg_username = current_username
            await user.save()

        data["user"] = user
        return await handler(event, data)
