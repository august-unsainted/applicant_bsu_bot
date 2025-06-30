from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.start import handle_message
from utils.calculator import get_speciality, get_buttons_states, edit_keyboard
from utils.data import generate_kb, keyboards

router = Router()

back_kb = generate_kb('calculator')


@router.callback_query(F.data.in_({'calculator', 'tip'}))
async def calculator(callback: CallbackQuery, state: FSMContext):
    kb = back_kb if callback.data == 'tip' else (await state.get_data()).get('subjects')
    await handle_message(callback, {'reply_markup': kb} if kb else None)


@router.callback_query(F.data.startswith('subject'))
async def handle_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=edit_keyboard(callback))


@router.callback_query(F.data == 'calculator_result')
async def get_calculator_result(callback: CallbackQuery, state: FSMContext):
    buttons = get_buttons_states(callback.message.reply_markup)
    speciality = get_speciality(buttons)
    if not speciality:
        await callback.answer(f'Нет специальностей 😢')
    elif len(speciality) >= 4096:
        await callback.answer(f'Выбрано слишком много предметов. Попробуйте еще раз')
    else:
        await state.update_data(subjects=callback.message.reply_markup)
        await handle_message(callback, {'text': speciality, 'reply_markup': keyboards.get(callback.data)})
