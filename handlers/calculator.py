from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.calculator import generate_keyboard, calculator_tip_kb, calculator_back_kb
from utils.calculator import get_speciality

router = Router()


@router.callback_query(F.data == 'calculator')
async def calculator(callback: CallbackQuery, state: FSMContext):
    if not (user_buttons_state := await state.get_data()):
        user_buttons_state = {f"subject_{i}": False for i in range(1, 12)}
        await state.update_data(buttons_state=user_buttons_state)
        user_buttons_state = {'buttons_state': user_buttons_state}
    await callback.message.edit_text('Выберите предметы:',
                                     reply_markup=generate_keyboard(user_buttons_state['buttons_state']))


@router.callback_query(F.data.startswith('subject'))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    buttons_state = user_data.get('buttons_state', {f"subject_{i}": False for i in range(1, 12)})

    if callback.data == 'subject_next':
        speciality = get_speciality(user_data)
        if speciality and len(speciality) < 4096:
            await callback.message.edit_text(speciality, parse_mode='HTML', reply_markup=calculator_tip_kb)
        elif not speciality:
            await callback.answer(f'Нет специальностей 😢')
        else:
            await callback.answer(f'Выбрано слишком много предметов. Попробуйте еще раз')
    else:
        buttons_state[callback.data] = not buttons_state[callback.data]
        await state.update_data(buttons_state=buttons_state)
        await callback.message.edit_reply_markup(reply_markup=generate_keyboard(buttons_state))


@router.callback_query(F.data == 'tip')
async def get_tip(callback: CallbackQuery):
    await callback.message.edit_text(
        '<b>Заголовок:</b> Факультет или институт, где вы будете учиться\n\n'
        '<b>Подзаголовок:</b> Специальность (направление)\n\n'
        '<b>Подпункт:</b> Профиль этой специальности\n\n'
        '<b>Код направления:</b> XX.YY.ZZ\n'
        '• XX — область (01 — математика, 04 — химия и т. д.)\n'
        '• YY — уровень образования (03 — бакалавриат, 05 — специалитет)\n'
        '• ZZ — номер направления (01, 02 и т. д.)\n\n'
        '<b>Форма обучения:</b>\n'
        '• Очная — учёба проходит в университете, занятия проходят каждый день.\n'
        '• Заочная — можно совмещать учёбу с работой, занятия обычно проходят в формате сессий.\n\n'
        '<b>Бакалавриат или специалитет?</b>\n'
        '• Бакалавриат (код направления 03): учёба длится 4 года. После выпуска можно поступить в магистратуру или сразу работать.\n'
        '• Специалитет (код направления 05): учёба длится 5–6 лет. Выпускники получают квалификацию специалиста и могут работать, например, врачом или инженером.\n\n'
        '<b>Пример:</b>\n\n'
        '<b>Химический факультет</b>\n'
        '<blockquote>Экология и природопользование (05.03.06, очно):\n'
        '    — Экологический мониторинг</blockquote>\n\n'
        '<b>Факультет</b>: Химический факультет\n'
        '<b>Специальность</b>: Экология и природопользование\n'
        '<b>Код направления</b>: 05.03.06 (очная форма обучения)\n'
        '  • 05 — область: науки о Земле (экология, геология)\n'
        '  • 03 — уровень: бакалавриат (4 года)\n'
        '  • 06 — конкретное направление: Экология и природопользование.\n'
        '<b>Форма обучения</b>: Очная — занятия каждый день.\n'
        '<b>Профиль</b>: Экологический мониторинг (контроль состояния окружающей среды).\n\n'
        '<a href="https://ulan-ude.postupi.online/vuz/bgu-ulan-ude/specialnosti/bakalavr/">Подробнее</a>',
        parse_mode='HTML',
        reply_markup=calculator_back_kb,
        disable_web_page_preview=True)
