import orjson
from pathlib import Path
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from utils.filesystem import create_input_file, find_resource_path


def get_back(needle: str) -> str | None:
    for key, value in keyboards_text.items():
        for callback in value.keys():
            if callback == needle:
                return key


def create_row(kb: list, callback: str, text: str = 'Назад ⬅️') -> None:
    kb.append([InlineKeyboardButton(callback_data=callback, text=text)])


def generate_kb(back_callback: str = None, data: dict[str, str] = None) -> InlineKeyboardMarkup:
    kb = []
    if data:
        [create_row(kb, callback, text) for callback, text in data.items()]
    if back_callback:
        create_row(kb, back_callback)
    return InlineKeyboardMarkup(inline_keyboard=kb)


def generate_dict_kb(data: dict[str, dict[str, str]]) -> dict[str, InlineKeyboardMarkup]:
    kbs = {}
    for key, kb in data.items():
        back = None if key.endswith(('start', 'stat', 'broadcast')) else get_back(key)
        kbs[key] = generate_kb(back, kb)
    kbs['calculator'] = generate_calculator_kb(kbs.get('calculator'))
    kbs['stat'] = InlineKeyboardMarkup(inline_keyboard=[[row[0] for row in kbs.get('stat').inline_keyboard]])
    return kbs


def generate_calculator_kb(calculator_kb: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    subjects = {f"subject_{i}": name for i, name in enumerate(specialties_text.get('subjects'), 1)}
    keyboard, arr = [], []
    for key, selected in {f"subject_{i}": False for i in range(1, len(subjects) + 1)}.items():
        text = f'✅ {subjects[key]}' if selected else subjects[key]
        arr.append(InlineKeyboardButton(text=text, callback_data=key))

    length = len(arr) - len(arr) % 2
    for i in range(0, length, 2):
        keyboard.append([arr[i], arr[i + 1]])
    if not length % 2:
        keyboard.append([arr[-1]])
    keyboard.extend(calculator_kb.inline_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def load_images() -> dict:
    imgs = {}
    src_dir = Path(find_resource_path('data/images'))
    for root, _, files in src_dir.walk():
        for file in files:
            fsinput = create_input_file('data/images/' + file)
            file = file[:-4]
            imgs[file] = InputMediaPhoto(media=fsinput, caption=messages_text.get(file), parse_mode='HTML')
            if file == 'start':
                imgs['cmd_start'] = fsinput

    return imgs


def get_paths(*paths: str) -> list:
    json_dir = Path(__file__).parent.parent / 'data/json'
    result = []
    for path in paths:
        full_path = json_dir / f'{path}.json'
        result.append(orjson.loads(full_path.read_bytes()))
    return result


def load_messages():
    images = load_images()
    default_args = {'parse_mode': 'HTML', 'disable_web_page_preview': True}
    messages_args = {
        'cmd_start': {
            'photo':      images.get('cmd_start'), 'caption': messages_text.get('start'),
            'reply_markup': keyboards.get('start'), **default_args
        }
    }
    for callback in messages_text.keys():
        args = {**default_args, 'reply_markup': keyboards.get(callback) or generate_kb(get_back(callback))}
        if images.get(callback):
            args['media'] = images.get(callback)
        else:
            args['text'] = messages_text.get(callback)
        messages_args[callback] = args
    return messages_args


messages_text, keyboards_text, specialties_text, stats = get_paths('messages', 'keyboards', 'specialties', 'stats')
keyboards = generate_dict_kb(keyboards_text)
specialties = {tuple(key.split(', ')): value for key, value in specialties_text.get('specialties').items()}
stats = stats.get('stats')
messages = load_messages()
