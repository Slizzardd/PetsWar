from typing import Tuple

from models.farm_data import UserFarmData
from models.user import User
from service import farm_service


async def start_farm(user: User) -> Tuple['UserFarmData', int]:
    farm_data = await user.get_farm_data()
    farm_data, income = await farm_service.make_farm(farm_data)
    return farm_data, income
