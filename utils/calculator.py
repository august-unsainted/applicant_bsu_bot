from collections import defaultdict
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from utils.data import specialties as data


def edit_keyboard(callback: CallbackQuery):
    callback, keyboard = callback.data, callback.message.reply_markup
    for row in keyboard.inline_keyboard:
        for btn in row:
            btn_callback = btn.callback_data
            if btn_callback == callback:
                row_ind = keyboard.inline_keyboard.index(row)
                btn_ind = row.index(btn)
                if btn.text.startswith('✅'):
                    new_text = btn.text.replace('✅ ', '')
                else:
                    new_text = '✅ ' + btn.text

                keyboard.inline_keyboard[row_ind][btn_ind].text = new_text
    return keyboard


def get_buttons_states(keyboard: InlineKeyboardMarkup) -> dict[str, bool]:
    result = {}
    for row in keyboard.inline_keyboard:
        for btn in row:
            btn_callback = btn.callback_data
            if btn_callback.startswith('subject'):
                result[btn_callback] = btn.text.startswith('✅')
    return result


def get_speciality(btns: dict):
    selected_keys = [key.replace('subject_', '') for key, selected in btns.items() if selected]
    if not selected_keys:
        return

    grouped = defaultdict(lambda: defaultdict(list))
    for key, value in data.items():
        if not set(key).issubset(set(selected_keys)):
            continue
        for institute, specialties in value.items():
            for specialty, directions in specialties.items():
                grouped[institute][specialty].extend(directions)

    result = []
    for institute, specialities in sorted(grouped.items()):
        specialities_str = []
        for speciality, directions in sorted(specialities.items()):
            directions_str = '\n'.join([f'    — {direction}' for direction in sorted(list(set(directions)))])
            specialities_str.append(f"{speciality}:\n{directions_str}" if directions_str else speciality)
        result.append(f"<b>{institute}</b><blockquote>{'\n\n'.join(specialities_str)}</blockquote>")

    return "\n\n".join(result)
