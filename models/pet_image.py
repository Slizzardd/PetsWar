from tortoise import fields
from tortoise.models import Model


class PetImage(Model):
    id = fields.IntField(pk=True)

    pet_type = fields.CharField(max_length=100, null=False)
    pet_element = fields.CharField(max_length=100, null=False)
    image_url = fields.CharField(max_length=200, null=False)

    class Meta:
        table = 'pet_image'
