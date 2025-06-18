import asyncio
import logging

from aiogram import Dispatcher, Bot
from tortoise import Tortoise, connections

from callback import pet_callback, error_callback, duel_callback, quest_callback
from config.bot_config import BOT_TOKEN
from config.database_config import DB_NAME, DB_PORT, DB_HOST, DB_USER, DB_PASSWORD
from handlers import command_handler, event_handler, message_handler, farm_handler, error_handler, admin_handler, \
    pet_handler, duel_handler, quest_handler
from middleware.reg_middleware import AutoRegisterMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    try:
        await Tortoise.init(
            db_url=f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
            modules={'models': [
                'models.user',
                'models.pet_duel',
                'models.pet_image',
                'models.user_level',
                'models.pet_duel_state',
                'models.quest'
            ]}
        )
        await Tortoise.generate_schemas()
        dp.include_routers(
            command_handler.router,
            event_handler.router,
            message_handler.router,
            farm_handler.router,
            error_handler.router,
            admin_handler.router,
            pet_handler.router,
            duel_handler.router,
            quest_handler.router,

            pet_callback.router,
            error_callback.router,
            duel_callback.router,
            quest_callback.router
        )
        dp.message.middleware(AutoRegisterMiddleware())

        await dp.start_polling(bot)
    finally:
        await connections.close_all()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
