import data.main_data as data
from dto.pet_with_buffs import PetDto
from exception.exceptions import NotEnoughBalance
from models.Pet import Pet
from models.type.animal import Animal
from models.type.element_name import ElementName
from models.user import User
from service import user_service, farm_service, pet_service


async def summon_new_pet(tg_id: int) -> Pet:
    user = await user_service.find_user_by_tg_id(tg_id)
    farm_data = await user.get_farm_data()
    if farm_service.has_enough_balance(farm_data):
        farm_data.balance -= data.PRISE_FOR_SUMMON
        await farm_service.update_farm(farm_data)
        pet = await pet_service.summon_new_pet(user)
        return pet
    else:
        raise NotEnoughBalance(f"❌ Для этой операции требуется {data.PRISE_FOR_SUMMON} лапкоин(-а), "
                               f"а у тебя сейчас только {farm_data.balance}.\n"
                               "Попробуй снова позже — фарм идёт каждые 2 часа! ⏳💰"
                               "Сделать это можно командой: 'пет фарм'"
                               )


async def update_nickname_of_pet(user: User, nickname: str) -> Pet:
    pet = await user.get_pet()
    pet.nickname = nickname
    pet = await pet_service.update_pet(pet)
    return pet


async def get_pet_from_user(user: User) -> Pet:
    pet = await pet_service.get_pet_by_user(user)
    return pet


async def get_photo_pet(pet_type: Animal, pet_element: ElementName) -> str:
    pet_type_str = pet_type.value
    pet_element_str = pet_element.value
    photo = await pet_service.get_photo_pet(pet_type_str, pet_element_str)
    return photo


async def get_pet_with_buffs(user: User) -> PetDto:
    pet = await user.get_pet()
    user_level = await user.get_level()

    pet_dto = PetDto(pet.animal, pet.element, user_level.level)

    return pet_dto


async def get_start_pet(user: User) -> Pet:
    pet = await pet_service.summon_new_pet(user)
    return pet
