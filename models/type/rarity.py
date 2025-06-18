from enum import Enum


class Rarity(Enum):
    COMMON = "Обычный"
    RARE = "Редкий"
    EPIC = "Эпический"
    LEGENDARY = "Легендарный"
    GOD = "Божественный"


@property
def name_ru(self):
    return self.value


# Привязываем свойства к классу
Rarity.name_ru = name_ru
