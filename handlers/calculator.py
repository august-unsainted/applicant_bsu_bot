from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.calculator import generate_keyboard, calculator_back_kb
from utils.calculator import buttons_state, get_speciality

router = Router()


@router.callback_query(F.data == 'calculator')
async def calculator(callback: CallbackQuery):
    await callback.message.edit_text('Выберите предметы:', reply_markup=generate_keyboard())


@router.callback_query(F.data.startswith('subject'))
async def handle_callback(callback: CallbackQuery):
    if callback.data == 'subject_next':
        speciality = get_speciality()
        if speciality and len(speciality) < 4096:
            await callback.message.edit_text(speciality, reply_markup=calculator_back_kb)
        elif not speciality:
            await callback.answer(f'Нет специальностей 😢')
        else:
            await callback.answer(f'Выбрано слишком много предметов. Попробуйте еще раз')
    else:
        buttons_state[callback.data] = not buttons_state[callback.data]
        await callback.message.edit_reply_markup(reply_markup=generate_keyboard())
