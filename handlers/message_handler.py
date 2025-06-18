from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

import config.bot_commands as commands
import config.emoji as ej
from facade import user_facade, pet_facade
from models.user import User
from util.message_helper import get_ling_by_user

router = Router()


@router.message(F.text.lower().startswith(commands.USER_PROFILE_TRIGGER))
async def user_profile(message: Message):
    target_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    user = await user_facade.get_user_by_tg_id(target_id)
    pet = await user.get_pet()
    pet_with_buffs = await pet_facade.get_pet_with_buffs(user)
    level = await user.get_level()
    # Форматируем дату присоединения в удобный формат (например, ДД.ММ.ГГГГ)
    joined_date = user.created.strftime("%d.%m.%Y")

    # Проверяем, есть ли питомец
    if not pet:
        await message.answer(
            f"{ej.PROFILE_EMOJI} Профиль игрока {get_ling_by_user(user)}\n\n"
            f"{ej.CREATE_EMOJI} Присоединился: {joined_date}\n"
            f"{ej.LEVEL_EMOJI} Уровень: {level.level}\n"
            f"{ej.LEVEL_PROGRESS_EMOJI} Прогресс: {level.experience} / {level.exp_to_next_level()} XP\n\n"
            f"{ej.WARN_EMOJI} У игрока пока нет питомца. Чтобы начать игру, он может получить стартового питомца командой 'пет начало'"
            , parse_mode=ParseMode.HTML
            , disable_web_page_preview=True)
        return

    pet_photo = await pet_facade.get_photo_pet(pet_type=pet.animal, pet_element=pet.element)

    await message.reply_photo(
        photo=pet_photo,
        caption=(
            f"{ej.PROFILE_EMOJI} Профиль игрока {get_ling_by_user(user)}\n\n"
            f"{ej.CREATE_EMOJI} Присоединился: {joined_date}\n"
            f"{ej.LEVEL_EMOJI} Уровень: {level.level}\n"
            f"{ej.LEVEL_PROGRESS_EMOJI} Прогресс: {level.experience} / {level.exp_to_next_level()} XP\n\n"
            f"{ej.PET_IMAGE} <b>Питомец:</b>\n"
            f"{ej.NICKNAME_EMOJI} <b>Кличка:</b> {pet.nickname}\n"
            f"{ej.TYPE_IMAGE} <b>Тип:</b> {pet_with_buffs.animal_name} ({pet_with_buffs.animal_rarity})\n"
            f"{ej.ELEMENT_EMOJI} <b>Элемент:</b> {pet_with_buffs.element_name} ({pet_with_buffs.element_rarity})\n"
            f"️{ej.DAMAGE_EMOJI} <b>Базовый урон:</b> {pet_with_buffs.base_damage} <b>Урон:</b> {pet_with_buffs.damage} \n"
            f"{ej.HEALTH_EMOJI} <b>Базовое здоровье:</b> {pet_with_buffs.base_health} <b>Здоровье:</b> {pet_with_buffs.health} \n"
            f"{ej.DESCRIPTION_EMOJI} Описание: {pet.animal.description}"
        ), parse_mode=ParseMode.HTML
    )


@router.message(F.text.lower().startswith(commands.GET_START_PET))
async def get_start_pet(message: Message, user: User):
    pet = await user.pet
    if pet:
        await message.reply(f'{ej.WARN_EMOJI} У вас уже есть питомец {ej.WARN_EMOJI}')
        return
    pet = await pet_facade.get_start_pet(user)
    pet_with_buffs = await pet_facade.get_pet_with_buffs(user)
    photo = await pet_facade.get_photo_pet(pet_type=pet.animal, pet_element=pet.element)
    await message.reply_photo(caption=(
        "Ваш питомец\n"
        f"{ej.NICKNAME_EMOJI} Кличка: {pet.nickname}\n"
        f"{ej.PET_IMAGE} Питомец: {pet_with_buffs.animal_name} ({pet_with_buffs.animal_rarity})\n"
        f"{ej.ELEMENT_EMOJI} Элемент: {pet_with_buffs.element_name} ({pet_with_buffs.element_rarity})\n"
        f"️{ej.DAMAGE_EMOJI} Базовый урон: {pet_with_buffs.base_damage} Урон: {pet_with_buffs.damage} \n"
        f"{ej.HEALTH_EMOJI} Базовое здоровье: {pet_with_buffs.base_health} Здоровье: {pet_with_buffs.health} \n"
        f"{ej.DESCRIPTION_EMOJI} Описание: {pet.animal.description}"
        f"\n\n"
        f"{ej.WARN_EMOJI} Отныне, вы можете получить питомца только призвав его, это можно сделать командой: 'пет призыв'\n"
        f"для этого вам потребуется 100 лапкоинов"),
        photo=photo
    )
