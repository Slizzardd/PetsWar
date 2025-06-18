import random

from data.main_data import HEALTH_GROWS_RATE, HEALTH_PER_LEVEL, DAMAGE_GROWS_RATE, DAMAGE_PER_LEVEL
from models.type.element_name import ElementName


# async def get_income_for_farm_coins() -> int:
#     return random.randint(30, 100)  # включительно от 30 до 100

async def get_income_for_farm_coins() -> int:
    return random.randint(99999, 999999)  # включительно от 30 до 100


async def generate_damage_with_element(
        start_damage: int,
        attacker_element: ElementName,
        defender_element: ElementName
) -> int:
    """
    Генерирует урон с учётом элементов.
    Если атакующий элемент силён против защищающегося — +20% урона.
    Если слаб — -20% урона.
    Добавляется случайный разброс ±15%.
    """

    damage = start_damage
    print('Начальный урон: ', damage)
    # Проверяем отношения элементов
    if defender_element in attacker_element.strong_against:
        damage = int(damage * 1.2)  # +20%
    elif defender_element in attacker_element.weak_against:
        damage = int(damage * 0.8)  # -20%

    print('Урон после стихий: ', damage)
    # Добавляем разброс ±15%
    variation = 0.15
    min_damage = int(damage * (1 - variation))
    max_damage = int(damage * (1 + variation))
    final_damage = random.randint(min_damage, max_damage)

    print('Урон после разброса: ', final_damage)
    return final_damage


def calculate_pet_health(base_health: int, level: int) -> int:
    """
    Рассчитывает здоровье питомца с учётом уровня.

    :param base_health: базовое здоровье питомца
    :param level: уровень пользователя
    :param growth_rate: процентный рост здоровья (например, 0.1 для 10%)
    :param health_per_level: дополнительное здоровье за каждый уровень
    :return: итоговое здоровье питомца
    """
    health = base_health * (1 + HEALTH_GROWS_RATE * (level - 1)) + level * HEALTH_PER_LEVEL
    return int(health)


def calculate_pet_damage(base_damage: int, level: int) -> int:
    """
    Рассчитывает урон питомца с учётом уровня.

    :param base_damage: базовый урон питомца
    :param level: уровень пользователя
    :param growth_rate: процентный рост урона (например, 0.07 для 7%)
    :param damage_per_level: дополнительный урон за каждый уровень
    :return: итоговый урон питомца
    """
    damage = base_damage * (1 + DAMAGE_GROWS_RATE * (level - 1)) + level * DAMAGE_PER_LEVEL
    return int(damage)
