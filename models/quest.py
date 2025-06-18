from tortoise import fields
from tortoise.models import Model

from exception.exceptions import UserNotRegistered
from models.type.quest_status import QuestStatus
from models.type.quest_type import QuestType
from models.user import User


class Quest(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="quests")
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    quest_type = fields.CharEnumField(QuestType)
    difficulty = fields.IntField()
    reward_exp = fields.IntField()
    reward_coins = fields.IntField()
    amount = fields.IntField()
    action_type = fields.CharField(max_length=255)
    status = fields.CharEnumField(QuestStatus)
    progress = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    finished_at = fields.DatetimeField(null=True)

    class Meta:
        table = 'quests'

    async def get_user(self) -> User | None:
        user = await self.user  # Pet или None
        if user:
            return user
        else:
            raise UserNotRegistered('У квеста нет пользователя(хз как такое вообще возможно)"')