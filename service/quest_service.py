from datetime import datetime, timedelta, timezone

from exception.exceptions import QuestCooldownError
from models.quest import Quest
from models.type.quest_status import QuestStatus
from models.user import User


async def create_quest_for_user(user: User, quest_data) -> Quest:
    quest = await Quest.create(user=user, status=QuestStatus.AWAITING, **quest_data)
    return quest


async def get_quest_by_id(quest_id: int) -> Quest:
    quest = await Quest.get(id=quest_id)
    return quest


async def update_quest(quest: Quest):
    await quest.save()
    return quest


async def can_accept_new_quest(user_id: int) -> None:
    last_finished_quest = await Quest.filter(
        user_id=user_id,
        finished_at__not_isnull=True
    ).order_by('-finished_at').first()

    if not last_finished_quest:
        return

    now_utc = datetime.now(timezone.utc)  # aware datetime с UTC

    time_passed = now_utc - last_finished_quest.finished_at

    remaining = timedelta(hours=1) - time_passed
    total_seconds = int(remaining.total_seconds())

    if time_passed < timedelta(hours=2):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        raise QuestCooldownError(
            f"Новый квест можно брать через {hours} час(а) {minutes} минут {seconds} секунд."
        )
