from models.user import User
from models.user_level import UserLevel


async def create_level(user: User) -> UserLevel:
    level = await UserLevel.create(
        user=user
    )
    return level


async def income_exp(level: UserLevel, amount: int) -> UserLevel:
    level.experience += amount
    if level.experience >= level.exp_to_next_level():
        level.experience -= level.exp_to_next_level()
        level.level += 1
    await level.save()
    return level
