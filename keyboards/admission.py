from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admission_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приём документов', callback_data='admission_documents')],
    [InlineKeyboardButton(text='Схема поступления', callback_data='about_scheme')],
    [InlineKeyboardButton(text='Формы обучения и требования', callback_data='admission_forms_and_requirements')],
    [InlineKeyboardButton(text='«Байкальская перспектива»', callback_data='about_olympiad')],
    [InlineKeyboardButton(text='Пробный ЕГЭ', callback_data='admission_exams')],
    [InlineKeyboardButton(text='Полезные ссылки', callback_data='admission_links')],
    [InlineKeyboardButton(text='Калькулятор ЕГЭ', callback_data='calculator')]
])

admission_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='admission_start')]])
