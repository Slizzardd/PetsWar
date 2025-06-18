from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import config.callback_commands as callback_command
from models.type.animal import Animal
from models.type.element_name import ElementName


def get_actions_for_wallet_button(tg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐉 Призвать нового питомца",
                                  callback_data=f"{callback_command.SUMMON_NEW_PET}:{tg_id}")]

        ],
    )


def build_confirm_summon_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, призвать",
                                     callback_data=f"{callback_command.CONFIRM_SUMMON_NEW_PET}:{tg_id}"),
                InlineKeyboardButton(text="❌ Нет, отмена",
                                     callback_data=f"{callback_command.CANCEL_SUMMON_NEW_PET}:{tg_id}"),
            ]

        ],
    )


def build_actions_after_summon_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Призвать следующего",
                                     callback_data=f"{callback_command.CONFIRM_SUMMON_NEW_PET}:{tg_id}")
            ]

        ],
    )


def build_accept_fight_keyboard(duel_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, принять",
                                     callback_data=f"{callback_command.ACCEPT_FIGHT}:{duel_id}"),
                InlineKeyboardButton(text="❌ Нет, отклонить",
                                     callback_data=f"{callback_command.CANCEL_FIGHT_OFFER}:{duel_id}"),
            ]

        ],
    )


def build_decline_duel(duel_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Отклонить",
                                     callback_data=f"{callback_command.CANCEL_FIGHT_OFFER}:{duel_id}"),
            ]

        ],
    )


def build_confirm_fight_offer_keyboard(duel_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, уверен",
                                     callback_data=f"{callback_command.CONFIRM_FIGHT_OFFER}:{duel_id}"),
                InlineKeyboardButton(text="❌ Нет, не уверен",
                                     callback_data=f"{callback_command.CANCEL_FIGHT_OFFER}:{duel_id}"),
            ]

        ],
    )


def build_choose_pet_type() -> ReplyKeyboardMarkup:
    all_russian_types = [animal.value for animal in Animal]

    # Создаём кнопки
    buttons = [KeyboardButton(text=name) for name in all_russian_types]

    # Группируем по 2 кнопки в ряд
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    # Создаём клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=True  # можно убрать, если хочешь оставить клаву
    )

    return keyboard


def build_choose_pet_element() -> ReplyKeyboardMarkup:
    all_russian_elements = [element.value for element in ElementName]

    # Создаём кнопки
    buttons = [KeyboardButton(text=name) for name in all_russian_elements]

    # Группируем по 2 кнопки в ряд
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    # Создаём клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=True  # можно убрать, если хочешь оставить клаву
    )

    return keyboard


def build_actions_in_duel(duel_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ударить",
                                     callback_data=f"{callback_command.KICK_FIGHT}:{duel_id}"),
                InlineKeyboardButton(text="Пропустить ход",
                                     callback_data=f"{callback_command.MISS_STEP_FIGHT}:{duel_id}"),
            ]

        ],
    )


def generate_link_to_bot() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 Открыть бота",
                url="https://t.me/PetsWar_bot?start=start"
            )
        ]
    ])


def build_actions_for_quest(quest_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ Принять",
                                     callback_data=f"{callback_command.ACCEPT_QUEST}:{quest_id}"),
                InlineKeyboardButton(text="❌ Отклонить",
                                     callback_data=f"{callback_command.DECLINE_QUEST}:{quest_id}"),
            ]

        ],
    )


def try_complete_quest(quest_id: int, action: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ {action}",
                                     callback_data=f"{callback_command.TRYING_COMPLETE}:{quest_id}"),
            ],
            [
                InlineKeyboardButton(text="❌ Отклонить квест",
                                     callback_data=f"{callback_command.DECLINE_QUEST}:{quest_id}"),
            ]

        ],
    )
