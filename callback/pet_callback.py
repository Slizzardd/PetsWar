from aiogram import Router, F
from aiogram.types import CallbackQuery

import config.emoji as ej
import keyboards.keyboards as kb
from config import callback_commands
from facade import pet_facade

router = Router()


async def check_button_owner(callback: CallbackQuery, button_owner_id: int) -> bool:
    """
    Проверяет, совпадает ли ID пользователя с ID владельца кнопки.
    Если нет — отправляет предупреждение и возвращает False.
    """
    if button_owner_id != callback.from_user.id:
        await callback.answer(
            text="Ай-ай-ай, это кнопка не для тебя",
            show_alert=True
        )
        return False
    return True


@router.callback_query(F.data.startswith(f"{callback_commands.SUMMON_NEW_PET}"))
async def summon_new_pet_prompt(callback: CallbackQuery):
    """Обработчик нажатия на кнопку призыва нового питомца — подтверждение."""
    button_owner = int(callback.data.split(":")[1])

    if not await check_button_owner(callback, button_owner):
        return

    await callback.message.reply(
        f"{ej.WARN_EMOJI} Ты уверен, что хочешь призвать нового питомца?\n\n"
        "Твой текущий питомец будет удалён и заменён новым.",
        reply_markup=kb.build_confirm_summon_keyboard(button_owner)
    )
    await callback.answer()


@router.callback_query(F.data.startswith(f"{callback_commands.CONFIRM_SUMMON_NEW_PET}"))
async def summon_new_pet_confirm(callback: CallbackQuery):
    """Обработчик подтверждения призыва нового питомца."""
    button_owner = int(callback.data.split(":")[1])

    if not await check_button_owner(callback, button_owner):
        return

    pet = await pet_facade.summon_new_pet(button_owner)
    photo = await pet_facade.get_photo_pet(pet.animal, pet.element)
    caption = (
        f"{ej.NICKNAME_EMOJI} Кличка: {pet.nickname}\n"
        f"{ej.PET_IMAGE} Животное: {pet.animal.name_ru} ({pet.animal.rarity.name_ru})\n"
        f"{ej.ELEMENT_EMOJI} Элемент: {pet.element.name_ru} ({pet.element.rarity.name_ru})\n"
        f"{ej.DAMAGE_EMOJI} Базовый урон: {pet.animal.damage}\n"
        f"{ej.HEALTH_EMOJI} Базовое здоровье: {pet.animal.health}\n"
        f"{ej.DESCRIPTION_EMOJI} Описание: {pet.animal.description}"
    )
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=caption,
        reply_markup=kb.build_actions_after_summon_keyboard(button_owner)
    )
    await callback.answer()


@router.callback_query(F.data.startswith(f"{callback_commands.CANCEL_SUMMON_NEW_PET}"))
async def summon_new_pet_cancel(callback: CallbackQuery):
    """Обработчик отмены призыва нового питомца."""
    button_owner = int(callback.data.split(":")[1])

    if not await check_button_owner(callback, button_owner):
        return

    await callback.message.answer("Очень жаль")
    await callback.answer()
