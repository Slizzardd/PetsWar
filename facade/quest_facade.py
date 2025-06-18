from models.quest import Quest
from models.type.quest_status import QuestStatus
from models.user import User
from service import quest_service, farm_service, level_service
from util.quest_generate import generate_procedural_quest
from datetime import datetime, timezone, timedelta


async def generate_quest(user: User) -> Quest:
    user_level = await user.get_level()
    quest_data = await generate_procedural_quest(user_level.level)
    quest = await quest_service.create_quest_for_user(user, quest_data)
    return quest


async def get_quest_by_id(quest_id: int) -> Quest:
    quest = await quest_service.get_quest_by_id(quest_id)
    return quest


async def check_quest(quest: Quest) -> Quest:
    quest.progress += 1
    if quest.progress == quest.amount:
        quest.status = QuestStatus.FINISHED
        quest.finished_at = datetime.now(timezone.utc)
        user = await quest.get_user()

        # пополнение баланса
        farm_data = await user.get_farm_data()
        await farm_service.income_balance(farm_data, quest.reward_coins)

        # пополнение опыта
        level = await user.get_level()
        await level_service.income_exp(level, quest.reward_exp)
    quest = await quest_service.update_quest(quest)
    return quest


async def accept_quest(quest: Quest) -> Quest:
    user = await quest.user
    await quest_service.can_accept_new_quest(user.id)
    quest.status = QuestStatus.ACCEPTED
    quest = await quest_service.update_quest(quest)
    return quest


async def decline_quest(quest: Quest) -> Quest:
    quest.status = QuestStatus.DECLINE
    quest = await quest_service.update_quest(quest)
    return quest


async def failed_quest(quest: Quest) -> Quest:
    quest.status = QuestStatus.FAILED
    quest.finished_at = datetime.now(timezone.utc)
    quest = await quest_service.update_quest(quest)
    return quest
