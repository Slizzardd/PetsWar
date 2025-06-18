import re

from aiogram import Bot
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

import config.bot_commands as cmd
import keyboards.keyboards as kb
from facade import duel_facade
from models.user import User
from service import user_service

router = Router()


@router.message(F.text.lower().startswith(cmd.START_FIGHT_HANDLER))
async def start_fight(message: Message, user: User, bot: Bot):
    text = message.text[len(cmd.START_FIGHT_HANDLER):].strip()
    match = re.match(r'@([\w_]+)', text)
    if not match:
        await message.answer("❗ Укажи Telegram username через @, например: `@some_user`", parse_mode="Markdown")
        return
    username = match.group(1)

    await user.get_pet()
    opponent = await user_service.find_user_by_tg_username(username)
    await opponent.get_pet()

    duel = await duel_facade.create_offer_for_duel(user.tg_id, username, str(message.chat.id))

    await bot.send_message(
        chat_id=message.from_user.id
        , text=(
            f'Вы уверены что хотите вызвать игрока "<a href=\"https://t.me/{duel.opponent.tg_username}\">{duel.opponent.tg_username}</a>" '
            f'на дуэль питомцев?'
        )
        , reply_markup=kb.build_confirm_fight_offer_keyboard(duel.id)
        , parse_mode=ParseMode.HTML
        , disable_web_page_preview=True
    )
