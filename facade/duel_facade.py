from facade import pet_facade
from models.pet_duel import PetDuel, DuelStatus
from models.pet_duel_state import PetDuelState
from models.user import User
from service import user_service, duel_service
from util.generate_random_helper import generate_damage_with_element


async def create_offer_for_duel(challenger_tg_id: int, opponent_tg_username: str, from_chat_id: str):
    challenger = await user_service.find_user_by_tg_id(challenger_tg_id)
    opponent = await user_service.find_user_by_tg_username(opponent_tg_username)

    new_duel = PetDuel()
    new_duel.challenger = challenger
    new_duel.opponent = opponent
    new_duel.from_chat_id = from_chat_id

    return await duel_service.create_pet_duel(new_duel)


async def find_duel_by_id(duel_id: int) -> PetDuel:
    duel = await duel_service.find_duel_by_id(duel_id)
    return duel


async def cancel_duel(duel_id: int) -> PetDuel:
    duel = await duel_service.find_duel_by_id(duel_id)
    duel.status = DuelStatus.DENIED
    updated_duel = await duel_service.update_duel(duel)
    return updated_duel


async def accept_duel(duel_id: int) -> PetDuel:
    duel = await duel_service.find_duel_by_id(duel_id)
    duel.status = DuelStatus.ACCEPTED
    updated_duel = await duel_service.update_duel(duel)
    return updated_duel


async def start_duel(duel: PetDuel) -> PetDuelState:
    # Загружаем связанные объекты challenger и opponent
    await duel.fetch_related("challenger", "opponent")
    challenger = await duel.challenger
    opponent = await duel.opponent
    challenger_pet = await pet_facade.get_pet_with_buffs(challenger)
    opponent_pet = await pet_facade.get_pet_with_buffs(opponent)

    new_state = PetDuelState()
    new_state.opponent_health = opponent_pet.health
    new_state.challenger_health = challenger_pet.health
    new_state.duel = duel
    new_state.current_turn = duel.challenger  # теперь это безопасно

    state = await duel_service.start_duel(new_state)
    return state


async def kick_in_duel(state: PetDuelState) -> tuple[PetDuelState, int, User, bool]:
    attacker = await state.current_turn
    attacker_pet = await pet_facade.get_pet_with_buffs(attacker)

    duel = await state.duel
    await duel.fetch_related("challenger", "opponent")

    duel_finished = False  # 🔹 по умолчанию дуэль не завершена

    # Определяем, кто защищается и его питомца
    if duel.challenger.id == attacker.id:
        defender = duel.opponent
        defender_pet = await defender.get_pet()
    else:
        defender = duel.challenger
        defender_pet = await defender.get_pet()

    # Генерируем урон с учётом элементов
    damage = await generate_damage_with_element(
        start_damage=attacker_pet.damage,
        attacker_element=attacker_pet.element,
        defender_element=defender_pet.element
    )

    # Применяем урон к здоровью защитника
    if defender.id == duel.opponent.id:
        state.opponent_health -= damage
        if state.opponent_health <= 0:
            duel.winner = attacker
            duel.status = DuelStatus.FINISHED
            duel_finished = True
    else:
        state.challenger_health -= damage
        if state.challenger_health <= 0:
            duel.winner = attacker
            duel.status = DuelStatus.FINISHED
            duel_finished = True

    if not duel_finished:
        # Передаём ход другому игроку
        state.current_turn = defender
        await state.save()
    else:
        # Сохраняем и состояние и саму дуэль
        await duel.save()
        await state.save()

    return state, damage, attacker, duel_finished

