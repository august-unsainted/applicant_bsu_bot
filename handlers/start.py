from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from config import ADMIN
from utils.db import add_user, increase_stat_count, get_stats, count_users
from utils.filesystem import images, create_image
from utils.data import generate_kb, messages, keyboards, keyboards_text, stats

router = Router()


async def handle_message(callback: CallbackQuery, kb: InlineKeyboardMarkup = None, text: str = '') -> None:
    kb = kb or keyboards.get(callback.data)
    if images.get(callback.data):
        await callback.message.edit_media(images.get(callback.data).get('input'), reply_markup=kb,
                                          disable_web_page_preview=True)
    else:
        args = {'text': messages.get(callback.data) or text, 'parse_mode': 'HTML', 'reply_markup': kb}
        if callback.message.text:
            await callback.message.edit_text(**args)
        else:
            await callback.message.answer(**args)
            try:
                await callback.message.delete()
            except TelegramBadRequest:
                pass


def get_back(needle: str) -> str | None:
    for key, value in keyboards_text.items():
        for callback in value.keys():
            if callback == needle:
                return key


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(photo=images['start']['fsinput'], caption=messages.get('start'), parse_mode='HTML',
                               reply_markup=keyboards.get('start'))
    await add_user(message.from_user.id)


@router.callback_query()
async def start(callback: CallbackQuery):
    if callback.data in stats:
        await increase_stat_count(callback.data)
    kb = keyboards.get(callback.data) or generate_kb(get_back(callback.data))
    await handle_message(callback, kb)


@router.message(F.chat.id != ADMIN)
async def any_message(message: Message):
    await message.answer('К сожалению, я не понимаю, что вы хотите сказать 😢')
    await message.delete()
