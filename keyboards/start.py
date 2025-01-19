from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приемная кампания (2025 г.)', callback_data='admission')],
    [InlineKeyboardButton(text='Общежития', callback_data='dormitories')],
    [InlineKeyboardButton(text='Байкальская перспектива', callback_data='olympiad')],
    [InlineKeyboardButton(text='Пробный ЕГЭ', callback_data='exams')],
    [InlineKeyboardButton(text='Полезные ссылки', callback_data='links')],
    [InlineKeyboardButton(text='О разработчиках', callback_data='developers')]
])

start_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='start')]])

