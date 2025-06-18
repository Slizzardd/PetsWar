from aiogram import Router, F
from aiogram.types import Message

import config.bot_commands as cmd
import keyboards.keyboards as kb
from facade import quest_facade
from models.user import User
from util import quest_generate

router = Router()


@router.message(F.text.lower().startswith(cmd.CREATE_QUEST_TRIGGER))
async def grow_level(message: Message, user: User):
    quest = await quest_facade.generate_quest(user)
    level = await user.get_level()
    chance_to_complete = await quest_generate.get_chance_for_complete_quest(quest.difficulty, level.level)
    text = (
        f"🧭 *Квест:* {quest.title}\n"
        f"📜 *Описание:* {quest.description}\n"
        f"🎯 *Тип:* {quest.quest_type.value.capitalize()}\n"
        f"🔥 *Сложность:* {quest.difficulty}/10\n"
        f"🔥 *Необходимо кол-во:* {quest.amount}\n"
        f"🎁 *Награда:* {quest.reward_exp} опыта, {quest.reward_coins} лапкоинов\n"
        f"🤞 *Шанс на выполнение:* {chance_to_complete}%\n"
    )

    await message.answer(text, parse_mode="Markdown", reply_markup=kb.build_actions_for_quest(quest.id))
