from enum import Enum


class QuestStatus(Enum):
    ACCEPTED = "Принят"
    AWAITING = "Ожидает подтверждения"
    FINISHED = "Завершен"
    DECLINE = "Отклонен"
    FAILED = 'Провален'
