import sys
from pathlib import Path
from aiogram.types import FSInputFile


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
