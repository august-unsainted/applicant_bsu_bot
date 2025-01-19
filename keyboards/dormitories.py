from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dormitories_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Этапы заселения', callback_data='stages')],
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='start')],
    ])
    
dormitories_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='dormitories')]])
