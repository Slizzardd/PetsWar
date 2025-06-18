from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exception.exceptions import NotEnoughBalance, BalanceNotFound, UserNotRegistered, QuestCooldownError

router = Router()


@router.error(ExceptionTypeFilter(NotEnoughBalance))
async def handle_not_enough_balance(event: ErrorEvent):
    error_text = str(event.exception)
    message = event.update.callback_query.message
    await event.update.callback_query.answer()
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(BalanceNotFound))
async def handle_not_enough_balance(event: ErrorEvent):
    error_text = str(event.exception)
    message = event.update.callback_query.message
    await event.update.callback_query.answer()
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(UserNotRegistered))
async def handle_not_enough_balance(event: ErrorEvent):
    error_text = str(event.exception)
    message = event.update.callback_query.message
    await event.update.callback_query.answer()
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(QuestCooldownError))
async def handle_not_enough_balance(event: ErrorEvent):
    error_text = str(event.exception)
    message = event.update.callback_query.message
    await event.update.callback_query.answer()
    await message.reply(error_text)
