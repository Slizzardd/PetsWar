from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

import config.emoji as ej
import keyboards.keyboards as kb
from config import callback_commands
from facade import quest_facade
from models.type.quest_status import QuestStatus
from util import quest_generate

router = Router()


def get_quest_id_from_request(callback: CallbackQuery) -> int:
    return int(callback.data.split(":")[1])


async def is_user_authorized(callback: CallbackQuery, user_id: int) -> bool:
    """Проверяет, что кнопка нажата нужным игроком"""
    if callback.from_user.id != user_id:
        await callback.answer(f"{ej.ERROR_EMOJI} Эта кнопка не для тебя! {ej.ERROR_EMOJI}", show_alert=True)
        return False
    return True


@router.callback_query(F.data.startswith(f"{callback_commands.ACCEPT_QUEST}"))
async def accept_quest(callback: CallbackQuery):
    quest_id = get_quest_id_from_request(callback)
    quest = await quest_facade.get_quest_by_id(quest_id)
    user = await quest.get_user()
    level = await user.get_level()
    if not await is_user_authorized(callback, user.tg_id):
        return

    quest = await quest_facade.accept_quest(quest)
    await callback.message.reply('Квест принят, для его выполнения, '
                                 'пожалуйста, перейдите в ЛС с ботом')

    chance_to_complete = await quest_generate.get_chance_for_complete_quest(quest.difficulty, level.level)
    await callback.bot.send_message(
        chat_id=user.tg_id,
        text=(
            f"🧭 Квест: {quest.title}\n"
            f"📜 Описание: {quest.description}\n"
            f"🎯 Тип: {quest.quest_type.value.capitalize()}\n"
            f"🔥 Сложность: {quest.difficulty}/10\n"
            f"🔥 Необходимо кол-во: {quest.amount}\n"
            f"🎁 Награда: {quest.reward_exp} опыта, {quest.reward_coins} лапкоинов\n"
            f"🤞 *Шанс на выполнение:* {chance_to_complete}%\n"
        ),
        reply_markup=kb.try_complete_quest(quest_id=quest_id, action=quest.action_type),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(F.data.startswith(f"{callback_commands.TRYING_COMPLETE}"))
async def trying_complete(callback: CallbackQuery):
    quest_id = get_quest_id_from_request(callback)
    quest = await quest_facade.get_quest_by_id(quest_id)
    user = await quest.get_user()

    if not await is_user_authorized(callback, user.tg_id):
        return

    if quest.status != QuestStatus.ACCEPTED:
        await callback.answer(f"{ej.ERROR_EMOJI} Этот квест уже закончен или ещё не принят! {ej.ERROR_EMOJI}",
                              show_alert=True)
        return

    level = await user.get_level()
    chance = await quest_generate.get_chance_for_complete_quest(quest.difficulty, level.level)
    is_success = await quest_generate.trying_complete(chance)
    if is_success:
        quest = await quest_facade.check_quest(quest)
        if quest.status == QuestStatus.FINISHED:
            text = (
                f"🧭 Квест: {quest.title}\n"
                f"📜 Описание: {quest.description}\n"
                f"🎯 Тип: {quest.quest_type.value.capitalize()}\n"
                f"🔥 Сложность: {quest.difficulty}/10\n"
                f"🔥 Необходимо количество: {quest.amount}\n"
                f"🎁 Награда: {quest.reward_exp} опыта, {quest.reward_coins} лапкоинов\n"
                f"{ej.STATUS_EMOJI} Статус: {quest.status.value}\n"
                f"Награды получены.\n"
                f"Следующий квест можно будет запросить через 1 час."
            )

            await callback.message.answer(text=text)
        else:
            await callback.message.answer(
                f"Ваш прогресс увеличился!\n"
                f"Текущий прогресс: {quest.progress} / {quest.amount}",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.try_complete_quest(quest_id=quest_id, action=quest.action_type)
            )

    else:
        await callback.message.answer(
            "😞 Вам не повезло, квест провален.\n"
            "Следующая попытка будет возможна только через 1 час."
        )
        await quest_facade.failed_quest(quest)
    await callback.answer()


@router.callback_query(F.data.startswith(f"{callback_commands.DECLINE_QUEST}"))
async def accept_quest(callback: CallbackQuery):
    quest_id = get_quest_id_from_request(callback)
    quest = await quest_facade.get_quest_by_id(quest_id)
    user = await quest.user

    if not await is_user_authorized(callback, user.tg_id):
        return

    if quest.status != QuestStatus.ACCEPTED:
        await callback.answer(f"{ej.ERROR_EMOJI} Этот квест уже закончен или ещё не принят! {ej.ERROR_EMOJI}",
                              show_alert=True)
        return

    quest = await quest_facade.decline_quest(quest)
    await callback.message.answer('Квест отклонен')
    await callback.answer()
