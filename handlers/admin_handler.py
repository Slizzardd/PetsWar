from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize

import config.bot_commands as cmd
import keyboards.keyboards as kb
from data.main_data import admins
from facade import admin_facade
from models.user import User
from states.states import CreatePetImage

router = Router()


# ---------------------Создание изображения для питомца--------------------------------------
@router.message(F.text.lower().startswith(cmd.CREATE_NEW_PET_IMAGE_TRIGGER), F.chat.type == 'private')
async def start_create_pet_image_step_one(message: Message, user: User, state: FSMContext) -> None:
    if user.tg_id not in admins:
        await message.answer('У тебя нет доступа к созданию питомцев')
        return

    await state.set_state(CreatePetImage.pet_type)
    await message.answer('Выберите название питомца: ',
                         reply_markup=kb.build_choose_pet_type())


@router.message(CreatePetImage.pet_type, F.chat.type == 'private')
async def start_create_pet_image_step_two(message: Message, user: User, state: FSMContext) -> None:
    if user.tg_id not in admins:
        await message.answer('У тебя нет доступа к созданию питомцев')
        return

    await state.update_data(pet_type=message.text)
    await state.set_state(CreatePetImage.pet_element)
    await message.answer('Выберите элемент питомца: ',
                         reply_markup=kb.build_choose_pet_element())


@router.message(CreatePetImage.pet_element, F.chat.type == 'private')
async def start_create_pet_image_step_three(message: Message, user: User, state: FSMContext):
    if user.tg_id not in admins:
        await message.answer('У тебя нет доступа к созданию питомцев')
        return

    await state.update_data(pet_element=message.text)
    await state.set_state(CreatePetImage.image_url)
    await message.answer('Пришлите изображение питомца')


@router.message(CreatePetImage.image_url, F.chat.type == 'private')
async def start_create_pet_image_step_four(message: Message, user: User, state: FSMContext) -> None:
    if user.tg_id not in admins:
        await message.answer('У тебя нет доступа к созданию питомцев')
        return

    if not message.photo:
        await message.answer('Пожалуйста, пришли изображение питомца (как фото, не как файл).')
        return

    largest_photo: PhotoSize = message.photo[-1]
    file_id = largest_photo.file_id

    await state.update_data(image_url=file_id)
    data = await state.get_data()
    await state.clear()

    pet = await admin_facade.create_new_pet_image(data)

    await message.reply_photo(caption=(
        "<b>✅ Изображение питомца успешно загружено!</b>\n\n"
        f"<i>Тип питомца:</i> <code>{pet.pet_type}</code>\n"
        f"<i>Стихия питомца:</i> <code>{pet.pet_element}</code>\n"),

        photo=pet.image_url,
        parse_mode=ParseMode.HTML
    )
