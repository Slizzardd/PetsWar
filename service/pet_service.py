import random

from tortoise.exceptions import DoesNotExist

from exception.exceptions import EntityNotFound
from models.Pet import Pet
from models.pet_image import PetImage
from models.type.animal import Animal, ANIMAL_RARITY
from models.type.element_name import ElementName
from models.type.rarity import Rarity
from models.user import User


async def summon_new_pet(user: User) -> Pet:
    element = choose_random_element()
    animal = choose_random_animal()
    try:
        pet = await Pet.get(user=user)
        pet.animal = animal
        pet.element = element
        await pet.save()
        return pet
    except DoesNotExist:
        pet = await Pet.create(
            user=user,
            animal=animal,
            element=element,
            nickname='123'
        )
        return pet


async def get_photo_pet(pet_type: str, pet_element: str) -> str:
    # 1. Пытаемся найти по обоим параметрам
    pet_image = await PetImage.filter(
        pet_type=pet_type,
        pet_element=pet_element
    ).first()

    if pet_image:
        return pet_image.image_url

    # 2. Если не найдено, ищем только по типу
    pet_image = await PetImage.filter(
        pet_type=pet_type
    ).first()

    if pet_image:
        return pet_image.image_url

    # 3. Если всё ещё нет — возвращаем дефолтную картинку
    return 'https://www.honey.kg/uploads/catalog/d3170647aa7587d065d82ca2e873af0e.jpg'


async def update_pet(pet: Pet):
    if pet:
        await pet.save()
        return pet
    else:
        raise EntityNotFound('Ваш питомец ещё не призван! '
                             '\nИспользуйте команду "призвать", чтобы начать приключение 🐉')


async def get_pet_by_user(user: User):
    pet = await user.pet
    if pet:
        return pet
    else:
        raise EntityNotFound('Ваш питомец ещё не призван! '
                             '\nИспользуйте команду "призвать", чтобы начать приключение 🐉')


def choose_rarity():
    rarities = [Rarity.COMMON, Rarity.RARE, Rarity.EPIC, Rarity.LEGENDARY]
    weights = [0.60, 0.25, 0.10, 0.05]
    return random.choices(rarities, weights=weights, k=1)[0]


def choose_random_animal() -> Animal:
    rarity = choose_rarity()
    candidates = [animal for animal in Animal if ANIMAL_RARITY.get(animal) == rarity]
    return random.choice(candidates)


def choose_random_element() -> ElementName:
    rarity = choose_rarity()
    candidates = [element for element in ElementName if element.rarity == rarity]
    return random.choice(candidates)
