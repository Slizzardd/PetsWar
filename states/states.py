from aiogram.fsm.state import StatesGroup, State


class GiveNickname(StatesGroup):
    id_pet = State()
    nickname_pet = State()


class CreatePetImage(StatesGroup):
    pet_type = State()
    pet_element = State()
    image_url = State()
