from aiogram import Router, F
from aiogram.types import Message

import config.bot_commands as cmd
import config.emoji as ej
import keyboards.keyboards as kb
from facade import pet_facade
from models.user import User

router = Router()


@router.message(F.text.lower().startswith(cmd.PET_PROFILE_TRIGGER))
async def cmd_profile(message: Message, user: User):
    pet = await user.get_pet()
    photo = await pet_facade.get_photo_pet(pet.animal, pet.element)
    pet_with_buffs = await pet_facade.get_pet_with_buffs(user)
    if pet:
        await message.reply_photo(caption=(
            "Ваш питомец\n"
            f"{ej.NICKNAME_EMOJI} Кличка: {pet.nickname}\n"
            f"{ej.PET_IMAGE} Животное: {pet_with_buffs.animal_name} ({pet_with_buffs.animal_rarity})\n"
            f"{ej.ELEMENT_EMOJI} Элемент: {pet_with_buffs.element_name} ({pet_with_buffs.element_rarity})\n"
            f"️{ej.DAMAGE_EMOJI} Базовый урон: {pet_with_buffs.base_damage} Урон: {pet_with_buffs.damage} \n"
            f"{ej.HEALTH_EMOJI} Базовое здоровье: {pet_with_buffs.base_health} Здоровье: {pet_with_buffs.health} \n"
            f"{ej.DESCRIPTION_EMOJI} Описание: {pet.animal.description}"),

            photo=photo
        )
    else:
        await message.reply('У вас ещё нет питомца, для его призыва вам нужно накопить 100 монет')


@router.message(F.text.lower().startswith(cmd.GIVE_NICKNAME_FOR_PET_TRIGGER))
async def cmd_give_nickname(message: Message, user: User):
    nickname = message.text[len(cmd.GIVE_NICKNAME_FOR_PET_TRIGGER):].strip()
    pet = await pet_facade.update_nickname_of_pet(user, nickname)
    pet_with_buffs = await pet_facade.get_pet_with_buffs(user)
    photo = await pet_facade.get_photo_pet(pet.animal, pet.element)
    await message.reply_photo(caption=(
        "Ваш обновленный питомец\n"
        f"{ej.NICKNAME_EMOJI} Кличка: {pet.nickname}\n"
        f"{ej.PET_IMAGE} Животное: {pet_with_buffs.animal_name} ({pet_with_buffs.animal_rarity})\n"
        f"{ej.ELEMENT_EMOJI} Элемент: {pet_with_buffs.element_name} ({pet_with_buffs.element_rarity})\n"
        f"️{ej.DAMAGE_EMOJI} Базовый урон: {pet_with_buffs.base_damage} Урон: {pet_with_buffs.damage} \n"
        f"{ej.HEALTH_EMOJI} Базовое здоровье: {pet_with_buffs.base_health} Здоровье: {pet_with_buffs.health} \n"
        f"{ej.DESCRIPTION_EMOJI} Описание: {pet.animal.description}"),

        photo=photo
    )


@router.message(F.text.lower().startswith(cmd.SUMMON_TRIGGER))
async def cmd_give_nickname(message: Message):
    await message.answer(f"{ej.WARN_EMOJI} Ты уверен, что хочешь призвать нового питомца?\n\n"
                         "Твой текущий питомец будет удалён и заменён новым.",
                         reply_markup=kb.build_confirm_summon_keyboard(message.from_user.id)
                         )
