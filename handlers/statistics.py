from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import ADMIN
from utils.data import keyboards
from utils.db import get_stats
from utils.filesystem import create_input_file

router = Router()

base_args = {'parse_mode': 'HTML', 'reply_markup': keyboards.get('stat')}


async def receive_stat(state: FSMContext) -> dict[str, str]:
    stat_months = await get_stats()
    await state.update_data(stat=stat_months)
    return {'text': stat_months[0], **base_args}


@router.message(Command('stat'), F.chat.id == ADMIN)
async def stat_cmd(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(**await receive_stat(state))


@router.message(Command('db'), F.chat.id == ADMIN)
async def db_cmd(message: Message):
    await message.delete()
    await message.answer_document(create_input_file('data/applicant.db'), caption='База данных <b>успешно</b> выгружена ✅', parse_mode='HTML')


@router.callback_query(F.data == 'stat')
async def stat(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(**await receive_stat(state))


@router.callback_query(F.data.startswith('stat'))
async def stat_scroll(callback: CallbackQuery, state: FSMContext):
    stats = (await state.get_data()).get('stat') or await get_stats()
    current = stats.index(callback.message.html_text)
    current += 1 if callback.data.endswith('forward') else -1
    if 0 <= current < len(stats):
        await callback.message.edit_text(stats[current], **base_args)
    else:
        await callback.answer('Больше значений нет 😢')
