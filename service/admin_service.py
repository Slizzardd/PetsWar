from tortoise.exceptions import DoesNotExist

from models.pet_image import PetImage


async def create_new_pet_image(pet_image: PetImage) -> PetImage:
    try:
        pet = await PetImage.get(pet_type=pet_image.pet_type, pet_element=pet_image.pet_element)
        pet.image_url = pet_image.image_url
        await pet.save()
        return pet
    except DoesNotExist:
        pet = await PetImage.create(
            pet_type=pet_image.pet_type,
            pet_element=pet_image.pet_element,
            image_url=pet_image.image_url
        )
        return pet
