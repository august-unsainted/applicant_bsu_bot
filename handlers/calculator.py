from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.calculator import generate_keyboard, calculator_back_kb
from utils.calculator import get_speciality

router = Router()


@router.callback_query(F.data == 'calculator')
async def calculator(callback: CallbackQuery, state: FSMContext):
    if not (user_buttons_state := await state.get_data()):
        user_buttons_state = {f"subject_{i}": False for i in range(1, 12)}
        await state.update_data(buttons_state=user_buttons_state)
        user_buttons_state = {'buttons_state': user_buttons_state}
    await callback.message.edit_text('Выберите предметы:', reply_markup=generate_keyboard(user_buttons_state['buttons_state']))


@router.callback_query(F.data.startswith('subject'))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    buttons_state = user_data.get('buttons_state', {f"subject_{i}": False for i in range(1, 12)})

    if callback.data == 'subject_next':
        speciality = get_speciality(user_data)
        if speciality and len(speciality) < 4096:
            await callback.message.edit_text(speciality, parse_mode='HTML', reply_markup=calculator_back_kb)
        elif not speciality:
            await callback.answer(f'Нет специальностей 😢')
        else:
            await callback.answer(f'Выбрано слишком много предметов. Попробуйте еще раз')
    else:
        buttons_state[callback.data] = not buttons_state[callback.data]
        await state.update_data(buttons_state=buttons_state)
        await callback.message.edit_reply_markup(reply_markup=generate_keyboard(buttons_state))
