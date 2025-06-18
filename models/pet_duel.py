from enum import Enum

from tortoise import fields, models

from models.pet_duel_state import PetDuelState


class DuelStatus(str, Enum):
    PENDING = "ожидает подтверждения"
    ACCEPTED = "подтвержден"
    FINISHED = "завершен"
    DENIED = "отклонен"


class PetDuel(models.Model):
    id = fields.IntField(pk=True)
    challenger = fields.ForeignKeyField("models.User", related_name="challenger_duels")
    opponent = fields.ForeignKeyField("models.User", related_name="opponent_duels")
    from_chat_id = fields.CharField(max_length=22)
    status = fields.CharEnumField(DuelStatus, max_length=21, default=DuelStatus.PENDING)
    winner = fields.ForeignKeyField("models.User", related_name="won_duels", null=True)

    state: fields.ReverseRelation["PetDuelState"]
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "pet_duels"

    async def get_state(self) -> PetDuelState | None:
        state = await self.state
        return state
