import os
import sys

console_colors = {
    "YELLOW": "\u001b[38;5;11m",
    "RESET": "\u001b[0m",
    "RED": "\u001b[31m",
    "GREEN": "\u001b[32m",
}


def output_message(text_red: str = None, text_yellow: str = None):
    """ Выводит в консоль сообщение об ошибке. """
    show_red = f"{console_colors['RED']}{text_red}{console_colors['RESET']}"
    show_yellow = f"{console_colors['YELLOW']}{text_yellow}{console_colors['RESET']}"
    print(f"{show_red}:\n\t-->> {show_yellow}")


def output_message_exit(text_red: str, text_yellow: str):
    """ Выводит в консоль сообщение об ошибке при чтении файла.
        Завершает приложение. """
    output_message(text_red, text_yellow)
    sys.exit()


def file_unused(abs_file_name: str) -> bool:
    """ Проверяет что файл не занят - не используется другим приложением. """
    if abs_file_name:
        if os.path.exists(abs_file_name):
            try:
                os.rename(abs_file_name, abs_file_name)
                return True
            except IOError:
                return False
        else:
            return True
    return False
