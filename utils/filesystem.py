import sys
from pathlib import Path
from aiogram.types import FSInputFile, InputMediaPhoto

from utils.data import messages

images = {}


def create_image(name: str, caption: str = '', file_id: str = '') -> InputMediaPhoto:
    return InputMediaPhoto(media=file_id or images.get(name), caption=caption or messages.get(name), parse_mode='HTML')


def create_input_file(path: Path | str) -> FSInputFile:
    path = find_resource_path(path)
    photo = FSInputFile(path=path)
    return photo


def find_resource_path(relative_path) -> str:
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).parent.parent
    return str(base_path / relative_path)


def _load_images():
    src_dir = Path(find_resource_path('data/images'))
    for root, _, files in src_dir.walk():
        for file in files:
            fsinput = create_input_file('data/images/' + file)
            file = file[:-4]
            images[file] = {
                'fsinput': fsinput,
                'input':   InputMediaPhoto(media=fsinput, caption=messages.get(file), parse_mode='HTML')
            }


_load_images()
