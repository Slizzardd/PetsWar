from tortoise import models

from exception.exceptions import DuelAlreadyExists
from models.pet_duel import PetDuel, DuelStatus
from models.pet_duel_state import PetDuelState


async def create_pet_duel(duel: PetDuel) -> PetDuel:
    # Проверка: участник уже участвует в активной дуэли?
    active_statuses = [DuelStatus.PENDING, DuelStatus.ACCEPTED]

    existing_duel = await PetDuel.filter(
        (models.Q(challenger=duel.challenger) | models.Q(opponent=duel.challenger) |
         models.Q(challenger=duel.opponent) | models.Q(opponent=duel.opponent)) &
        models.Q(status__in=active_statuses)
    ).first()

    if existing_duel:
        raise DuelAlreadyExists("Один из участников уже находится в активной дуэли.")

    # Создание новой дуэли
    return await PetDuel.create(
        challenger=duel.challenger,
        opponent=duel.opponent,
        from_chat_id=duel.from_chat_id,
        status=DuelStatus.PENDING
    )


async def find_duel_by_id(duel_id: int) -> PetDuel:
    duel = await PetDuel.get(id=duel_id).prefetch_related("challenger", "opponent")
    return duel


async def update_duel(duel: PetDuel) -> PetDuel:
    await duel.save()
    return duel


async def start_duel(new_state: PetDuelState) -> PetDuelState:
    state = await PetDuelState.create(
        challenger_health=new_state.challenger_health,
        opponent_health=new_state.opponent_health,
        current_turn=new_state.current_turn,
        duel = new_state.duel
    )
    return state