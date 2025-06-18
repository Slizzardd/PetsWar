from models.pet_image import PetImage
from service import admin_service


async def create_new_pet_image(data):
    new_pet_image = PetImage()
    new_pet_image.pet_type = data['pet_type']
    new_pet_image.pet_element = data['pet_element']
    new_pet_image.image_url = data['image_url']

    pet_image = await admin_service.create_new_pet_image(new_pet_image)
    return pet_image
