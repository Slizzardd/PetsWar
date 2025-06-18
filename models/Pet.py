from tortoise import fields, models, Model

from models.type.animal import Animal
from models.type.element_name import ElementName


class Pet(Model):
    id = fields.IntField(pk=True)

    user = fields.OneToOneField('models.User', related_name='pet', on_delete=fields.CASCADE)

    # Храним значение питомца из enum Animal как строку
    animal = fields.CharEnumField(Animal, max_length=32)

    # Элемент питомца (из enum ElementName)
    element = fields.CharEnumField(ElementName, max_length=50)

    # Кличка питомца (может задавать пользователь)
    nickname = fields.CharField(max_length=50)

    class Meta:
        table = "pets"
