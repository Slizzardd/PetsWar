from tortoise import fields
from tortoise.models import Model

from exception.exceptions import UserNotRegistered
from models.Pet import Pet
from models.farm_data import UserFarmData
from models.user_level import UserLevel


class User(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    tg_id = fields.BigIntField(unique=True)
    tg_username = fields.CharField(max_length=100, null=True)

    farm_data: fields.ReverseRelation["UserFarmData"]
    pet: fields.ReverseRelation["Pet"]
    level: fields.ReverseRelation["UserLevel"]

    class Meta:
        table = 'users'

    async def get_pet(self) -> Pet | None:
        pet = await self.pet  # Pet или None
        if pet:
            return pet
        else:
            raise UserNotRegistered('У пользователя нет питомца, ему нужно написать "Пет начало"')

    async def get_level(self) -> UserLevel | None:
        level = await self.level  # Pet или None
        if level:
            return level
        else:
            raise UserNotRegistered('У пользователя нет уровня, хз как так получилось')

    async def get_farm_data(self) -> UserFarmData | None:
        farm_data = await self.farm_data  # Pet или None
        if farm_data:
            return farm_data
        else:
            raise UserNotRegistered('У пользователя нет БАЛАНСА, хз как так получилось')
