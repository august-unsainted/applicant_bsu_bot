import orjson
from pathlib import Path
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_kb(back_callback: str = '', *buttons: list[str]) -> InlineKeyboardMarkup:
    kb = []
    for row in buttons:
        kb.append([InlineKeyboardButton(text=row[0], callback_data=row[1])])
    if back_callback:
        kb.append([InlineKeyboardButton(text='Назад ⬅️', callback_data=back_callback)])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def generate_dict_kb(data: dict[str, dict[str]]) -> dict[str, InlineKeyboardMarkup]:
    kbs = {}
    for key, value in data.items():
        inline_kb = []
        for callback, text in value.items():
            inline_kb.append([InlineKeyboardButton(text=text, callback_data=callback)])
        kbs[key] = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    return kbs


def generate_calculator_kb() -> InlineKeyboardMarkup:
    keyboard, arr = [], []
    for key, selected in {f"subject_{i}": False for i in range(1, len(subjects) + 1)}.items():
        text = f'✅ {subjects[key]}' if selected else subjects[key]
        arr.append(InlineKeyboardButton(text=text, callback_data=key))

    length = len(arr) - len(arr) % 2
    for i in range(0, length, 2):
        keyboard.append([arr[i], arr[i + 1]])
    if not length % 2:
        keyboard.append([arr[-1]])
    keyboard.extend(keyboards.get('calculator').inline_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_paths(*paths: str) -> list:
    json_dir = Path(__file__).parent.parent / 'data/json'
    result = []
    for path in paths:
        full_path = json_dir / f'{path}.json'
        result.append(orjson.loads(full_path.read_bytes()))
    return result


messages, keyboards_text, specialties_text, stats = get_paths('messages', 'keyboards', 'specialties', 'stats')
keyboards = generate_dict_kb(keyboards_text)
specialties = {tuple(key.split(', ')): value for key, value in specialties_text.get('specialties').items()}
subjects = {f"subject_{i}": name for i, name in enumerate(specialties_text.get('subjects'), 1)}
keyboards['calculator'] = generate_calculator_kb()
keyboards['stat'] = InlineKeyboardMarkup(inline_keyboard=[[row[0] for row in keyboards.get('stat').inline_keyboard]])
stats = stats.get('stats')
