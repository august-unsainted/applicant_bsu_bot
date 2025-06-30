from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from config import ADMIN
from utils.db import add_user, increase_stat_count
from utils.data import messages, stats

router = Router()


async def handle_text_edit(message: Message, args: dict):
    if message.text:
        response = await message.edit_text(**args)
    else:
        response = await message.answer(**args)
        try:
            await message.delete()
        except TelegramBadRequest:
            pass
    return response


async def handle_message(callback: CallbackQuery, additional: dict = None) -> None:
    args = messages.get(callback.data) or {'parse_mode': 'HTML', 'disable_web_page_preview': True}
    if additional:
        args = {**args, **additional}

    if args.get('media'):
        await callback.message.edit_media(**args)
    else:
        await handle_text_edit(callback.message, args)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(**messages.get('cmd_start'))
    await add_user(message.from_user.id)


@router.callback_query()
async def start(callback: CallbackQuery):
    if callback.data in stats:
        await increase_stat_count(callback.data)
    await handle_message(callback)


@router.message(F.chat.id != ADMIN)
async def any_message(message: Message):
    await message.answer('К сожалению, я не понимаю, что вы хотите сказать 😢')
    await message.delete()
