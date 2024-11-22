from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

scheme_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посещение БГУ', callback_data='scheme_visit_bsu')],
    [InlineKeyboardButton(text='Через систему БГУ (онлайн)', callback_data='scheme_bsu_system')],
    [InlineKeyboardButton(text='Через Госуслуги (онлайн)', callback_data='scheme_epgu')],
    [InlineKeyboardButton(text='Назад', callback_data='admission_start')]
])

scheme_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='about_scheme')]])
