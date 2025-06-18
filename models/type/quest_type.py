from enum import Enum


class QuestType(Enum):
    HUNT = "Охота"
    GATHER = "Сбор ресурсов"
    EXPLORE = "Разведка"
    BOSS = "Битва с боссом"
    ESCORT = "Эскорт"
    DELIVER = "Доставка"
    DEFENSE = "Защита"
    TRAINING = "Тренировка"
