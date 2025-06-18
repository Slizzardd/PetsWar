from tortoise import fields, models

from models.user import User


class PetDuelState(models.Model):
    id = fields.IntField(pk=True)
    duel = fields.OneToOneField("models.PetDuel", related_name="state", on_delete=fields.CASCADE)

    challenger_health = fields.IntField()
    opponent_health = fields.IntField()
    current_turn = fields.ForeignKeyField("models.User", related_name="+")

    class Meta:
        table = "pet_duel_states"

    async def get_opponent(self) -> User:
        duel = await self.duel
        await duel.fetch_related('challenger', 'opponent')

        if self.current_turn.id == duel.challenger.id:
            return duel.opponent
        else:
            return duel.challenger

    async def get_opponent_health(self) -> int:
        duel = await self.duel
        await duel.fetch_related('challenger', 'opponent')

        if self.current_turn.id == duel.challenger.id:
            return self.opponent_health
        else:
            return self.challenger_health

