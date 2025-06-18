import config.bot_commands as cmd
from exception.exceptions import FarmDataNotFound, EntityNotFound
from models.farm_data import UserFarmData
from models.user import User
from service import user_service, farm_service, level_service


async def get_farm_data_from_user(user: User) -> UserFarmData:
    farm_data = await user.get_farm_data()

    if farm_data is None:
        raise FarmDataNotFound(
            "🧑‍🌾 У вас ещё нет кошелька!\n"
            f"Начните фарм с команды '{cmd.FARM_TRIGGER}', чтобы получить первые лапкоины 💰"
        )

    return farm_data


async def create_user(username: str, tg_id: int) -> User:
    new_user = User()
    new_user.tg_id = tg_id
    new_user.tg_username = username

    user = await user_service.create_user(new_user)

    await farm_service.create_farm(user)

    await level_service.create_level(user)

    return user


async def get_user_by_tg_id(tg_id: id) -> User:
    try:
        user = await user_service.find_user_by_tg_id(tg_id)
        return user
    except ValueError:
        raise EntityNotFound("Этот пользователь не зарегистрирован в боте")
