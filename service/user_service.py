from tortoise.exceptions import DoesNotExist

from models.user import User


async def create_user(user: User) -> User:
    new_user = await User.create(
        tg_id=user.tg_id,
        tg_username=user.tg_username
    )

    return new_user


async def find_user_by_tg_id(tg_id: int) -> User:
    try:
        user = await User.get(tg_id=tg_id)
        return user
    except DoesNotExist:
        raise ValueError(f"Пользователь с tg_id @{tg_id} не найден")


async def find_user_by_tg_username(tg_username: str) -> User:
    try:
        user = await User.get(tg_username=tg_username)
        return user
    except DoesNotExist:
        raise ValueError(f"Пользователь с tg_username @{tg_username} не найден")
