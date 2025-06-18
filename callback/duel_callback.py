from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

import config.callback_commands as callback_cmd
import config.emoji as ej
import keyboards.keyboards as kb
from facade import duel_facade, pet_facade
from util.message_helper import get_ling_by_user

router = Router()


# -------------------- Общие вспомогательные функции --------------------

def get_duel_id_from_request(callback: CallbackQuery) -> int:
    return int(callback.data.split(":")[1])


async def is_user_authorized(callback: CallbackQuery, user_id: int) -> bool:
    """Проверяет, что кнопка нажата нужным игроком"""
    if callback.from_user.id != user_id:
        await callback.answer(f"{ej.ERROR_EMOJI} Эта кнопка не для тебя! {ej.ERROR_EMOJI}", show_alert=True)
        return False
    return True


# -------------------- Колбэки --------------------

@router.callback_query(F.data.startswith(callback_cmd.CONFIRM_FIGHT_OFFER))
async def handle_offer_for_duel_start(callback: CallbackQuery):
    duel_id = get_duel_id_from_request(callback)
    duel = await duel_facade.find_duel_by_id(duel_id)

    await callback.bot.send_message(
        chat_id=duel.opponent.tg_id
        , text=(
            f"{ej.DUEL_EMOJI} <b>Вызов на дуэль!</b>\n\n"
            f"{ej.PROFILE_EMOJI} {get_ling_by_user(duel.challenger)} "
            f"вызывает тебя на дуэль, @{duel.opponent.tg_username}!\n\n"
            f"Принять вызов?"
        )
        , reply_markup=kb.build_accept_fight_keyboard(duel.id)
        , parse_mode=ParseMode.HTML
        , disable_web_page_preview=True
    )

    await callback.bot.send_message(
        chat_id=duel.challenger.tg_id
        , text=(
            f'Запрос отправлен, если хотите отклонить запрос - нажмите кнопку'
        )
        , reply_markup=kb.build_decline_duel(duel.id)
        , parse_mode=ParseMode.HTML
        , disable_web_page_preview=True
    )
    await callback.answer()


@router.callback_query(F.data.startswith(callback_cmd.CANCEL_FIGHT_OFFER))
async def handle_offer_for_duel_cancel(callback: CallbackQuery):
    duel_id = get_duel_id_from_request(callback)
    # duel = await duel_facade.find_duel_by_id(duel_id)
    # #
    # # if not await is_user_authorized(callback, duel.challenger.tg_id):
    # #     return

    updated_duel = await duel_facade.cancel_duel(duel_id)
    await callback.message.answer(
        f"{ej.WARN_EMOJI} Дуэль была отменена.\n"
        f"{ej.STATUS_EMOJI} Статус: <b>{updated_duel.status.value}</b>",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    await callback.answer()


@router.callback_query(F.data.startswith(callback_cmd.ACCEPT_FIGHT))
async def handle_duel_accept(callback: CallbackQuery):
    duel_id = get_duel_id_from_request(callback)
    duel = await duel_facade.find_duel_by_id(duel_id)

    if not await is_user_authorized(callback, duel.opponent.tg_id):
        return

    duel = await duel_facade.accept_duel(duel_id)

    await callback.bot.send_message(
        chat_id=duel.from_chat_id
        , text=(
            f"{ej.DUEL_EMOJI} <b>Дуэль принята!</b>\n\n"
            f"{ej.PROFILE_EMOJI} {get_ling_by_user(duel.opponent)} принял вызов от {get_ling_by_user(duel.challenger)}.\n"
            f"Статус: <b>{duel.status.value}</b>\n"
            f"{ej.DUEL_EMOJI} <b>Дуэль начинается!</b>"
            f"{ej.FIRE_EMOJI} <b> Ждите результатов!!!</b> {ej.FIRE_EMOJI}"
        )
        , parse_mode=ParseMode.HTML
        , disable_web_page_preview=True
    )

    state = await duel_facade.start_duel(duel)

    opponent = await state.get_opponent()

    pet_with_buff = await pet_facade.get_pet_with_buffs(opponent)
    photo = await pet_facade.get_photo_pet(pet_with_buff.animal, pet_with_buff.element)
    await callback.bot.send_photo(
        chat_id=state.current_turn.tg_id
        , caption=(
            f"{ej.TURN_EMOJI} <b>Ваш ход!</b>\n\n"
            f"{ej.PET_IMAGE} <b>Питомец {get_ling_by_user(opponent)}:</b>\n"
            f"{ej.TYPE_IMAGE} <b>Тип:</b>  {pet_with_buff.animal_name} ({pet_with_buff.animal_rarity})\n"
            f"{ej.ELEMENT_EMOJI} <b>Элемент:</b> ️ {pet_with_buff.element_name} ({pet_with_buff.element_rarity})\n"
            f"{ej.HEALTH_EMOJI} <b>Здоровье:</b> ️ <code>{await state.get_opponent_health()} HP</code>\n"
            f"{ej.DAMAGE_EMOJI} <b>Урон:</b> <code>{pet_with_buff.damage}</code>\n\n"
            f"{ej.TURN_EMOJI} <b>Выберите действие:</b>"
        )
        , reply_markup=kb.build_actions_in_duel(duel_id)
        , parse_mode=ParseMode.HTML
        , photo=photo
    )
    await callback.answer()


@router.callback_query(F.data.startswith(callback_cmd.DISMISS_FIGHT))
async def handle_duel_dismiss(callback: CallbackQuery):
    duel_id = get_duel_id_from_request(callback)
    duel = await duel_facade.find_duel_by_id(duel_id)

    if not await is_user_authorized(callback, duel.opponent.tg_id):
        return

    duel = await duel_facade.cancel_duel(duel_id)
    await callback.message.answer(
        f"{ej.ERROR_EMOJI} <b>Дуэль отклонена.</b>\n\n"
        f"{get_ling_by_user(duel.opponent)} отклонил вызов {get_ling_by_user(duel.challenger)}.\n"
        f"{ej.STATUS_EMOJI} Статус: <b>{duel.status.value}</b>",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    await callback.answer()


@router.callback_query(F.data.startswith(callback_cmd.KICK_FIGHT))
async def kick_action_in_duel(callback: CallbackQuery):
    duel_id = get_duel_id_from_request(callback)
    duel = await duel_facade.find_duel_by_id(duel_id)
    state_duel = await duel.get_state()

    await state_duel.fetch_related('current_turn')

    if not await is_user_authorized(callback, state_duel.current_turn.tg_id):
        return

    # Выполняем удар
    new_state, damage, attacker, finished = await duel_facade.kick_in_duel(state_duel)

    if finished:
        winner = await new_state.current_turn
        duel = await new_state.duel
        await duel.fetch_related("challenger", "opponent")

        if duel.challenger.id == winner.id:
            loser = duel.opponent
        else:
            loser = duel.challenger

        # Получаем питомца победителя с баффами
        pet_with_buff = await pet_facade.get_pet_with_buffs(winner)

        # Отправляем сообщение победителю
        await callback.bot.send_message(
            chat_id=winner.tg_id,
            text=(
                f"{ej.CONGRATULATION_EMOJI} Поздравляем! Вы выиграли дуэль против {get_ling_by_user(loser)}.\n"
                "Отличная работа! Ваш питомец заслуженно победил."
            ),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

        # Отправляем сообщение проигравшему
        await callback.bot.send_message(
            chat_id=loser.tg_id,
            text=(
                f"{ej.DUEL_EMOJI} К сожалению, игрок {get_ling_by_user(winner)} выиграл эту дуэль.\n"
                "Не расстраивайтесь — следующий бой может быть вашим!"
            ),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

        # Отправляем сообщение в общий чат (duel.from_chat_id)
        await callback.bot.send_photo(
            chat_id=duel.from_chat_id,
            photo=await pet_facade.get_photo_pet(pet_with_buff.animal, pet_with_buff.element),
            caption=(
                f"{ej.CONGRATULATION_EMOJI} Игрок <b>{get_ling_by_user(winner)}</b> победил игрока <b>{get_ling_by_user(loser)}</b> "
                "в честной дуэли и заслуживает статус победителя! Побед на его счету: <b>n</b>.\n\n"
                f"{ej.PET_IMAGE} <b>Питомец победителя:</b>\n"
                f"{ej.TYPE_IMAGE} <b>Тип:</b> {pet_with_buff.animal_name} ({pet_with_buff.animal_rarity})\n"
                f"{ej.ELEMENT_EMOJI} <b>Элемент:</b> {pet_with_buff.element_name} ({pet_with_buff.element_rarity})\n"
                f"{ej.HEALTH_EMOJI} <b>Здоровье:</b> ️ <code>{pet_with_buff.health} HP</code>\n"
                f"{ej.DAMAGE_EMOJI} <b>Урон:</b> <code>{pet_with_buff.damage}</code>\n\n"
            ),
            parse_mode=ParseMode.HTML
        )

        await callback.answer()
        return

    duel = await new_state.duel
    await duel.fetch_related("challenger", "opponent")

    # Определяем, кто получил урон и его здоровье
    if duel.challenger.id == attacker.id:
        defender = duel.opponent
        new_health = new_state.opponent_health
    else:
        defender = duel.challenger
        new_health = new_state.challenger_health

    next_player = await new_state.current_turn

    # Сообщение для атакующего
    await callback.bot.send_message(
        chat_id=attacker.tg_id,
        text=(
            f"⚔️ Вы нанесли <b>{damage}</b> урона.\n"
            f"❤️ Текущее здоровье противника: <b>{new_health}</b>.\n\n"
            f"Теперь ходит <b>{get_ling_by_user(next_player)}</b>."
        ),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

    # Сообщение для получившего урон (защитника)
    await callback.bot.send_message(
        chat_id=defender.tg_id,
        text=(
            f"⚔️ Игрок <b>{get_ling_by_user(attacker)}</b> нанес вам <b>{damage}</b> урона.\n"
            f"❤️ Текущее здоровье вашего питомца: <b>{new_health}</b>.\n\n"
        ),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

    pet_with_buff = await pet_facade.get_pet_with_buffs(attacker)
    photo = await pet_facade.get_photo_pet(pet_type=pet_with_buff.animal, pet_element=pet_with_buff.element)
    await callback.bot.send_photo(
        chat_id=next_player.tg_id
        , caption=(
            "🎮 <b>Ваш ход!</b>\n\n"
            f"🐾 <b>Питомец {get_ling_by_user(attacker)}:</b>\n"
            f"• <b>Тип:</b> 🐉 {pet_with_buff.animal_name} ({pet_with_buff.animal_rarity})\n"
            f"• <b>Элемент:</b> ☠️ {pet_with_buff.element_name} ({pet_with_buff.element_rarity})\n"
            f"• <b>Здоровье:</b> ❤️ <code>{await new_state.get_opponent_health()} HP</code>\n"
            f"• <b>Урон:</b> 💥 <code>{pet_with_buff.damage}</code>\n\n"
            "⚔️ <b>Выберите действие:</b>"
        )
        , reply_markup=kb.build_actions_in_duel(duel_id)
        , parse_mode=ParseMode.HTML
        , photo=photo
    )
    await callback.answer()
