from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message

from exception.exceptions import FarmTimeNotPassed, FarmDataNotFound, EntityNotFound, DuelAlreadyExists, \
    UserNotRegistered, QuestCooldownError

router = Router()


@router.error(ExceptionTypeFilter(FarmTimeNotPassed), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(DuelAlreadyExists), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(QuestCooldownError), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(EntityNotFound), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)

    await message.reply(error_text)


@router.error(ExceptionTypeFilter(UserNotRegistered), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)

    await message.reply(error_text)


@router.error(ExceptionTypeFilter(FarmDataNotFound), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)
    await message.reply(error_text)


@router.error(ExceptionTypeFilter(ValueError), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)

    await message.answer(error_text)


@router.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    error_text = str(event.exception)
    await message.answer(error_text)
