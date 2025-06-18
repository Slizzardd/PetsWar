from enum import Enum
from models.type.rarity import Rarity


class Animal(Enum):
    KOBOLD = 'Кобольд'
    GOBLIN = 'Гоблин'
    FOREST_ELF = 'Лесной эльф'
    FAUN = 'Фавн'
    KITSUNE = 'Кицуне'

    HARPY = 'Гарпия'
    MERMAID = 'Русалка'
    NAGA = 'Нага'
    MANTICORE = 'Мантикора'
    PEGASUS = 'Пегас'

    DRAGON = 'Дракон'
    PHOENIX = 'Феникс'
    CERBERUS = 'Цербер'
    GRIFFIN = 'Грифон'
    VAMPIRE_CAT = 'Вампирская кошка'

    KRAKEN = 'Кракен'
    GORGON = 'Горгона'
    SNEAKING_TIGER = 'Тигр теней'
    FIREBIRD = 'Жар-птица'
    WYVERN = 'Виверна'

    EPHYRION = 'Эфирион'

    # --- Свойства ---

    @property
    def name_ru(self) -> str:
        return self.value

    @property
    def rarity(self) -> Rarity:
        return {
            Animal.KOBOLD: Rarity.COMMON,
            Animal.GOBLIN: Rarity.COMMON,
            Animal.FOREST_ELF: Rarity.COMMON,
            Animal.FAUN: Rarity.COMMON,
            Animal.KITSUNE: Rarity.COMMON,

            Animal.HARPY: Rarity.RARE,
            Animal.MERMAID: Rarity.RARE,
            Animal.NAGA: Rarity.RARE,
            Animal.MANTICORE: Rarity.RARE,
            Animal.PEGASUS: Rarity.RARE,

            Animal.DRAGON: Rarity.EPIC,
            Animal.PHOENIX: Rarity.EPIC,
            Animal.CERBERUS: Rarity.EPIC,
            Animal.GRIFFIN: Rarity.EPIC,
            Animal.VAMPIRE_CAT: Rarity.EPIC,

            Animal.KRAKEN: Rarity.LEGENDARY,
            Animal.GORGON: Rarity.LEGENDARY,
            Animal.SNEAKING_TIGER: Rarity.LEGENDARY,
            Animal.FIREBIRD: Rarity.LEGENDARY,
            Animal.WYVERN: Rarity.LEGENDARY,

            Animal.EPHYRION: Rarity.GOD
        }.get(self)

    @property
    def description(self) -> str:
        return {
            Animal.KOBOLD: "Маленькое подземное существо.",
            Animal.GOBLIN: "Проворный и хитрый пакостник.",
            Animal.FOREST_ELF: "Таинственный обитатель лесов.",
            Animal.FAUN: "Весёлое существо с копытами и рожками.",
            Animal.KITSUNE: "Магический лис из японских мифов.",

            Animal.HARPY: "Птица с женским лицом, парящая в небе.",
            Animal.MERMAID: "Морская дева с чарующим голосом.",
            Animal.NAGA: "Призрачная дева, возвещающая беду своим пронзительным криком.",
            Animal.MANTICORE: "Чудовище с телом льва и хвостом скорпиона.",
            Animal.PEGASUS: "Крылатый конь из легенд.",

            Animal.DRAGON: "Огнедышащее летающее чудовище.",
            Animal.PHOENIX: "Птица, возрождающаяся из пепла.",
            Animal.CERBERUS: "Трёхголовый пёс, страж подземного мира.",
            Animal.GRIFFIN: "Существо с телом льва и головой орла.",
            Animal.VAMPIRE_CAT: "Таинственная охотница ночи.",

            Animal.KRAKEN: "Огромное морское чудовище.",
            Animal.GORGON: "Существо, обращающее в камень взглядом.",
            Animal.SNEAKING_TIGER: "Невидимый охотник в темноте.",
            Animal.FIREBIRD: "Птица с сияющим оперением и магией.",
            Animal.WYVERN: "Дракон с двумя крыльями и хвостом-копьём.",

            Animal.EPHYRION: "Величественное божественное существо, олицетворяющее свет и чистоту эфира."
        }.get(self, "")

    @property
    def health(self) -> int:
        return {
            Animal.KOBOLD: 50,
            Animal.GOBLIN: 55,
            Animal.FOREST_ELF: 60,
            Animal.FAUN: 65,
            Animal.KITSUNE: 70,

            Animal.HARPY: 80,
            Animal.MERMAID: 85,
            Animal.NAGA: 90,
            Animal.MANTICORE: 95,
            Animal.PEGASUS: 100,

            Animal.DRAGON: 150,
            Animal.PHOENIX: 140,
            Animal.CERBERUS: 130,
            Animal.GRIFFIN: 120,
            Animal.VAMPIRE_CAT: 110,

            Animal.KRAKEN: 200,
            Animal.GORGON: 190,
            Animal.SNEAKING_TIGER: 180,
            Animal.FIREBIRD: 170,
            Animal.WYVERN: 160,

            Animal.EPHYRION: 250
        }.get(self, 0)

    @property
    def damage(self) -> int:
        return {
            Animal.KOBOLD: 10,
            Animal.GOBLIN: 12,
            Animal.FOREST_ELF: 14,
            Animal.FAUN: 13,
            Animal.KITSUNE: 15,

            Animal.HARPY: 20,
            Animal.MERMAID: 22,
            Animal.NAGA: 24,
            Animal.MANTICORE: 23,
            Animal.PEGASUS: 25,

            Animal.DRAGON: 40,
            Animal.PHOENIX: 38,
            Animal.CERBERUS: 36,
            Animal.GRIFFIN: 34,
            Animal.VAMPIRE_CAT: 32,

            Animal.KRAKEN: 50,
            Animal.GORGON: 48,
            Animal.SNEAKING_TIGER: 46,
            Animal.FIREBIRD: 44,
            Animal.WYVERN: 42,

            Animal.EPHYRION: 60
        }.get(self, 0)
