from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admission_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расписание приёма и контакты', callback_data='contacts')],
    [InlineKeyboardButton(text='Схема поступления', callback_data='scheme')],
    [InlineKeyboardButton(text='Калькулятор ЕГЭ', callback_data='calculator')],
    [InlineKeyboardButton(text='Формы обучения и требования', callback_data='forms')],
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='start')],
    ])
    
admission_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='admission')]])
