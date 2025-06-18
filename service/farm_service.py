from datetime import datetime, timezone, timedelta

import data.main_data as data
from exception.exceptions import FarmTimeNotPassed, BalanceNotFound
from models.farm_data import UserFarmData
from models.user import User
from util.generate_random_helper import get_income_for_farm_coins


async def create_farm(user: User) -> UserFarmData:
    farm_data = await UserFarmData.create(user=user)
    return farm_data


async def update_farm(farm: UserFarmData):
    await farm.save()


async def income_balance(farm: UserFarmData, amount: int) -> UserFarmData:
    farm.balance += amount
    await farm.save()
    return farm


async def make_farm(user_farm_data: UserFarmData) -> tuple[UserFarmData, int]:
    now = datetime.now(timezone.utc)

    # Первый фарм — разрешаем сразу
    if user_farm_data.last_farm_time is None:
        income = await get_income_for_farm_coins()
        user_farm_data.last_farm_time = now
        user_farm_data.balance += income
        await user_farm_data.save()
        return user_farm_data, income

    # Следующий фарм по таймеру
    next_farm_time = user_farm_data.last_farm_time + data.FARM_COOLDOWN

    if now >= next_farm_time:
        income = await get_income_for_farm_coins()
        user_farm_data.last_farm_time = now
        user_farm_data.balance += income
        await user_farm_data.save()
        return user_farm_data, income

    # Если еще рано — сообщаем об этом
    remaining = next_farm_time - now
    raise FarmTimeNotPassed(get_remaining_time_message(remaining))


def get_remaining_time_message(remaining: timedelta) -> str:
    total_seconds = int(remaining.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return (
        "⏳ Фарм пока недоступен.\n"
        f"Пройдёт ещё {hours} ч. {minutes} мин. {seconds} сек., прежде чем вы сможете снова фармить.\n"
        "Попробуйте позже 💪"
    )


def has_enough_balance(user_farm_data: UserFarmData) -> bool:
    try:
        if user_farm_data.balance >= data.PRISE_FOR_SUMMON:
            return True
        else:
            return False
    except Exception:
        raise BalanceNotFound('У вас ещё нет кошелька, создать его можно с помощью команды "пет фарм"')
