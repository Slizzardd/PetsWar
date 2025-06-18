from models.type.animal import Animal

QUEST_TEMPLATES = [
    {
        "type": "battle",
        "title": "Угроза в лесу!",
        "description_template": "Победи {amount} существ типа {enemy}.",
        "enemies": [Animal.GOBLIN.value, Animal.FOREST_ELF.value, Animal.NAGA.value],
        "amount_range": (3, 10),
        "reward_base": 20,
    },
    {
        "type": "collect",
        "title": "Сбор ресурсов",
        "description_template": "Собери {amount} {resource}.",
        "resources": ["лечебных трав", "магических грибов", "кристаллов маны"],
        "amount_range": (2, 5),
        "reward_base": 15,
    },
    # Добавляй шаблоны новых типов
]
