from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

olympiad_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Об этапах', callback_data='olympiad_rounds')],
    [InlineKeyboardButton(text='Профили', callback_data='olympiad_profiles')],
    [InlineKeyboardButton(text='Привилегии участников', callback_data='olympiad_privileges')],
    [InlineKeyboardButton(text='Контакты оргкомитета', callback_data='olympiad_contacts')],
    [InlineKeyboardButton(text='Документы', callback_data='olympiad_documents')],
    [InlineKeyboardButton(text='Соорганизаторы', callback_data='olympiad_organizers')],
    [InlineKeyboardButton(text='Назад', callback_data='admission_start')]])

olympiad_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='about_olympiad')]])
