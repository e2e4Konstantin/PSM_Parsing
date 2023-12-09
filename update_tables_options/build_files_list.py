import os
import re

from files_tolls import output_message_exit


def build_files_list_by_mask(files_path: str, mask: str) -> tuple[str, ...]:
    """ Создает кортеж из полных имен файлов по маске 'mask'. """

    xlsx_mask = re.compile(mask)
    files = [os.path.join(files_path, file) for file in os.listdir(files_path) if xlsx_mask.match(file)]
    if files:
        return tuple(files)
    else:
        output_message_exit(f"Фалы не найдены", f"{files!r}")
    return tuple()
