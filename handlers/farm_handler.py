from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

import config.bot_commands as cmd
import keyboards.keyboards as kb
from data import main_data
from facade import farm_facade
from models.user import User

router = Router()


@router.message(F.text.lower().startswith(cmd.FARM_TRIGGER))
async def cmd_farm(message: Message, user: User):
    farm_data, income = await farm_facade.start_farm(user)
    await message.reply(
        "🌾 Фарм прошёл успешно!\n"
        f"💰 Вы заработали: <b>{income}</b> {main_data.COIN_NAME}(а)\n"
        f"📦 Ваш текущий баланс: <b>{int(farm_data.balance)}</b> {main_data.COIN_NAME}(а)\n"
        f"Следующий фарм возможен через {main_data.FARM_COOLDOWN.total_seconds() // 3600} часа"
        , parse_mode=ParseMode.HTML)


@router.message(F.text.lower().startswith(cmd.BALANCE_TRIGGER))
async def cmd_balance(message: Message, user: User):
    farm_data = await user.get_farm_data()

    await message.reply(
        "💼 Ваш текущий баланс:\n"
        f"💰 <b>{int(farm_data.balance)}</b> {main_data.COIN_NAME}(а)"
        , parse_mode=ParseMode.HTML
        , reply_markup=kb.get_actions_for_wallet_button(user.tg_id))
