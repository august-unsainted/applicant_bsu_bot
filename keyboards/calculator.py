from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.calculator import subjects


def generate_keyboard(buttons_state):
    keyboard = []
    arr = []
    for key, selected in buttons_state.items():
        text = f'✅ {subjects[key]}' if selected else subjects[key]
        arr.append(InlineKeyboardButton(text=text, callback_data=key))
    for i in range(0, 11, 2):
        if i != len(arr) - 1:
            keyboard.append([arr[i], arr[i + 1]])
        else:
            keyboard.append([arr[i]])
    keyboard.append([InlineKeyboardButton(text='Далее', callback_data='subject_next')])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='admission_start')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


calculator_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='calculator')]
])
