from enum import Enum

from models.type.rarity import Rarity


class ElementName(Enum):
    FIRE = "Огонь"
    WATER = "Вода"
    WIND = "Ветер"
    EARTH = "Земля"
    FOREST = "Лес"
    LIGHTNING = "Гром"
    ICE = "Лёд"
    POISON = "Яд"
    METAL = "Металл"
    MAGMA = "Магма"
    ARCANE = "Аркана"
    COSMIC = "Космос"
    ABYSS = "Бездна"
    FATE = "Судьба"

    @property
    def name_ru(self):
        return self.value

    @property
    def rarity(self) -> Rarity:
        return ELEMENT_RARITY.get(self)

    @property
    def strong_against(self):
        return ELEMENT_STRONG_AGAINST.get(self, [])

    @property
    def weak_against(self):
        return ELEMENT_WEAK_AGAINST.get(self, [])


ELEMENT_RARITY = {
    ElementName.FIRE: Rarity.COMMON,
    ElementName.WATER: Rarity.COMMON,
    ElementName.WIND: Rarity.RARE,
    ElementName.EARTH: Rarity.COMMON,
    ElementName.FOREST: Rarity.RARE,
    ElementName.LIGHTNING: Rarity.EPIC,
    ElementName.ICE: Rarity.RARE,
    ElementName.POISON: Rarity.EPIC,
    ElementName.METAL: Rarity.RARE,
    ElementName.MAGMA: Rarity.EPIC,
    ElementName.ARCANE: Rarity.LEGENDARY,
    ElementName.COSMIC: Rarity.LEGENDARY,
    ElementName.ABYSS: Rarity.LEGENDARY,
    ElementName.FATE: Rarity.GOD,
}

ELEMENT_STRONG_AGAINST = {
    ElementName.FIRE: [ElementName.FOREST, ElementName.ICE],
    ElementName.WATER: [ElementName.FIRE, ElementName.MAGMA],
    ElementName.WIND: [ElementName.FIRE, ElementName.POISON],
    ElementName.EARTH: [ElementName.LIGHTNING, ElementName.METAL],
    ElementName.FOREST: [ElementName.EARTH, ElementName.WATER],
    ElementName.LIGHTNING: [ElementName.WATER, ElementName.FOREST],
    ElementName.ICE: [ElementName.WIND, ElementName.FOREST],
    ElementName.POISON: [ElementName.FOREST, ElementName.ABYSS],
    ElementName.METAL: [ElementName.ICE, ElementName.POISON],
    ElementName.MAGMA: [ElementName.METAL, ElementName.LIGHTNING],
    ElementName.ARCANE: [ElementName.ABYSS, ElementName.FATE],
    ElementName.COSMIC: [ElementName.ARCANE, ElementName.FATE],
    ElementName.ABYSS: [ElementName.COSMIC, ElementName.MAGMA],
    ElementName.FATE: [
        ElementName.FIRE, ElementName.WATER, ElementName.WIND,
        ElementName.EARTH, ElementName.FOREST, ElementName.LIGHTNING,
        ElementName.ICE, ElementName.POISON, ElementName.METAL,
        ElementName.MAGMA, ElementName.ARCANE, ElementName.COSMIC,
        ElementName.ABYSS
    ],
}

ELEMENT_WEAK_AGAINST = {
    ElementName.FIRE: [ElementName.WATER, ElementName.EARTH],
    ElementName.WATER: [ElementName.LIGHTNING, ElementName.FOREST],
    ElementName.WIND: [ElementName.ICE, ElementName.METAL],
    ElementName.EARTH: [ElementName.FOREST, ElementName.MAGMA],
    ElementName.FOREST: [ElementName.FIRE, ElementName.POISON],
    ElementName.LIGHTNING: [ElementName.EARTH, ElementName.MAGMA],
    ElementName.ICE: [ElementName.FIRE, ElementName.METAL],
    ElementName.POISON: [ElementName.WIND, ElementName.METAL],
    ElementName.METAL: [ElementName.MAGMA, ElementName.EARTH],
    ElementName.MAGMA: [ElementName.WATER, ElementName.ABYSS],
    ElementName.ARCANE: [ElementName.COSMIC, ElementName.ABYSS],
    ElementName.COSMIC: [ElementName.ABYSS, ElementName.FATE],
    ElementName.ABYSS: [ElementName.ARCANE, ElementName.POISON],
    ElementName.FATE: [],
}
