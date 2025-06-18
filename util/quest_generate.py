import random

from models.type.quest_type import QuestType

TITLES = {
    QuestType.HUNT: ["Охота на монстра", "Истребление тварей"],
    QuestType.GATHER: ["Сбор ресурсов", "Поиск полезных предметов"],
    QuestType.EXPLORE: ["Разведка территории", "Исследование неизвестного"],
    QuestType.BOSS: ["Битва с боссом", "Сразись с лидером врагов"],
    QuestType.ESCORT: ["Сопровождение", "Защита путника"],
    QuestType.DELIVER: ["Доставка посылки", "Передай груз"],
    QuestType.DEFENSE: ["Защита базы", "Отрази атаку"],
    QuestType.TRAINING: ["Тренировка навыков", "Повышение мастерства"]
}

ENEMIES = [
    "гоблина",
    "дракона",
    "разбойника",
    "тролля",
    "вампира",
    "оркa",
    "скелета",
    "зомби",
    "волколака",
    "черного мага",
    "демона",
    "ведьму",
    "дракончика"
]

ITEMS = [
    "целебную траву",
    "магический артефакт",
    "свиток древних",
    "зелье исцеления",
    "кристалл силы",
    "древний амулет",
    "редкий минерал",
    "волшебное перо",
    "золотой ключ",
    "зелье невидимости",
    "плащ теней",
    "меч искателя",
    "камень мудрости"
]

LOCATIONS = [
    "лес", "пещеру", "руины", "гора",
    "озеро", "болото", "долина", "плато",
    "пустыня", "холмы", "каньон", "замок",
    "деревня", "форт", "заброшенный храм"
]

NPCS = [
    "торговца",
    "посланника",
    "путника",
    "старейшину",
    "мага",
    "охотника",
    "ремесленника",
    "разведчика",
    "купца",
    "волшебника"
]

BASES = [
    "форт",
    "поселение",
    "засаду",
    "стражевую башню",
    "крепость",
    "лагерь",
    "городские ворота",
    "укреплённый мост",
    "рекрутскую казарму",
    "тайный штаб"
]


async def get_difficulty(user_level: int) -> int:
    base = min(10, max(1, user_level))
    options = list(range(1, 11))  # 1 до 10
    # Чем ближе к base, тем выше вес
    weights = [10 - abs(base - d) for d in options]
    return random.choices(options, weights=weights, k=1)[0]


async def generate_procedural_quest(user_level: int):
    quest_type = random.choice(list(QuestType))
    # base_difficulty = min(10, max(1, user_level))
    # difficulty = random.randint(
    #     max(1, base_difficulty - 2),
    #     min(10, base_difficulty + 2)
    # )
    difficulty = await get_difficulty(user_level)

    reward_exp = 50 + difficulty * 10
    reward_coins = 30 + difficulty * 5

    # Выбираем подходящий заголовок для типа квеста
    title = random.choice(TITLES.get(quest_type, ["Задание"]))

    if quest_type == QuestType.HUNT:
        target = random.choice(ENEMIES)
        amount = random.randint(2, 5)
        action_type = "Убить"
        description = f"Ты должен победить {amount} {target}(ов)."

    elif quest_type == QuestType.GATHER:
        target = random.choice(ITEMS)
        amount = random.randint(1, 3)
        action_type = "Собрать"
        description = f"Найди и принеси {amount} {target}(а)."

    elif quest_type == QuestType.EXPLORE:
        target = random.choice(LOCATIONS)
        amount = 1
        action_type = "Исследовать"
        description = f"Найди {target} и доложи о ситуации."

    elif quest_type == QuestType.BOSS:
        target = random.choice(ENEMIES)
        amount = 1
        action_type = "Победить"
        description = f"Победи босса — {target}."

    elif quest_type == QuestType.ESCORT:
        target = random.choice(NPCS)
        amount = 1
        action_type = "Сопроводить"
        description = f"Сопроводи {target} до безопасного места."

    elif quest_type == QuestType.DELIVER:
        target = random.choice(ITEMS)
        amount = 1
        action_type = "Доставить"
        description = f"Доставь {target} адресату."

    elif quest_type == QuestType.DEFENSE:
        target = random.choice(BASES)
        amount = 1
        action_type = "Защитить"
        description = f"Защити {target} от врагов."

    elif quest_type == QuestType.TRAINING:
        target = "тренировочную площадку"
        amount = 1
        action_type = "Тренироваться"
        description = f"Заверши тренировку на {target}."

    else:
        target = "???"
        amount = 1
        action_type = "Неизвестно"
        description = "Описание квеста недоступно."

    return {
        "title": title,
        "description": description,
        "quest_type": quest_type,
        "difficulty": difficulty,
        "reward_exp": reward_exp,
        "reward_coins": reward_coins,
        "target": target,
        "amount": amount,
        "action_type": action_type,
    }


async def trying_complete(chance: int) -> bool:
    # Рандом от 1 до 100
    roll = random.randint(1, 100)

    print(chance)
    return roll <= chance


async def get_chance_for_complete_quest(quest_difficulty: int, user_level: int) -> int:
    # Базовый шанс: от 90% (легко) до 10% (сложно)
    base_chance = max(1, 100 - quest_difficulty * 10)

    # Бонус за уровень игрока
    # Например: за каждый уровень выше сложности даём +1.5% к шансу
    level_bonus = max(0, int((user_level - quest_difficulty) * 1.5))

    # Общий шанс (но не более 95%)
    success_chance = min(95, base_chance + level_bonus)

    return success_chance
