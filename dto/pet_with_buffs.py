from data.main_data import HEALTH_PER_LEVEL, HEALTH_GROWS_RATE, DAMAGE_GROWS_RATE, DAMAGE_PER_LEVEL
from models.type.animal import Animal
from models.type.element_name import ElementName


class PetDto:
    def __init__(self, animal: Animal, element: ElementName, level: int = 1):
        self.animal = animal
        self.level = level
        self.element = element

    @property
    def animal_name(self):
        return self.animal.name_ru

    @property
    def animal_rarity(self):
        return self.animal.rarity.name_ru

    @property
    def element_name(self):
        return self.element.name_ru

    @property
    def element_rarity(self):
        return self.element.rarity.name_ru

    @property
    def base_health(self):
        return self.animal.health

    @property
    def base_damage(self):
        return self.animal.damage

    @property
    def health(self):
        return int(
            self.base_health * (1 + HEALTH_GROWS_RATE * (self.level - 1)) + self.level * HEALTH_PER_LEVEL
        )

    @property
    def damage(self):
        return int(
            self.base_damage * (1 + DAMAGE_GROWS_RATE * (self.level - 1)) + self.level * DAMAGE_PER_LEVEL
        )

